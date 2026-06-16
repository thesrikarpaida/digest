#!/usr/bin/env python3
"""
build_digest.py — build the security + AI digest for the Chirpy site.

It turns a large set of RSS/Atom feeds into a small, curated, de-duplicated set
of posts (the FEED / TOP PICKS / DEEP DIVES sections), summarized by an LLM.

Flow:
  1. Read feed URLs from feeds.txt (the full list). feeds-core.txt is a smaller
     trusted subset used only by the OpenRouter fallback.
  2. Fetch every feed concurrently (with per-host throttling so high-volume
     hosts like medium.com don't rate-limit us). Keep only entries inside the
     lookback window that aren't already in state/seen.json, newest first,
     capped to DIGEST_MAX_CANDIDATES.
  3. Curate with an LLM — Google Gemini by default (thinking disabled for
     speed), OpenRouter as an automatic fallback. The model selects the items
     that matter, rewrites each headline, writes a 3-6 sentence summary, and
     assigns severity, tags, a section ("feed" or "deep-dives"), and a
     must_know flag.
  4. Enforce the rules in CODE, not on trust: de-duplicate near-identical
     stories (shared CVE id or high title overlap), cap output to
     DIGEST_MAX_PUBLISH, and cap must_know ("Top Picks") to DIGEST_MAX_MUST_KNOW.
  5. Write each item into its own Jekyll collection at _digest/<run-date>/<slug>.md
     (a separate collection so the digest never shows up on the personal blog).
  6. Record every candidate considered in seen.json so it's never reprocessed.
     If every provider fails, publish NOTHING and leave the items unseen so the
     next run retries them (no half-baked junk on the live site) — unless
     DIGEST_ALLOW_RAW_FALLBACK=true, which permits un-curated link posts.

Config is via environment variables / a local .env file; see .env.example and
README.md for every knob. API keys are sent as request headers (never in a URL)
and scrubbed from all console/log output.

Run:  python build_digest.py            (writes posts)
      python build_digest.py --dry-run  (reports only; writes nothing)
      python build_digest.py --verbose  (also lists every unreachable feed)
"""

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
import re
import sys
import threading
import time
from pathlib import Path
from urllib.parse import urlparse

import feedparser
import requests
from dateutil import parser as dateparser

# ----------------------------------------------------------------------------
# Paths & config
# ----------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent          # .../blog
# Digest items go in their own collection (NOT _posts), so they don't show on
# the home/BLOG page. Each run writes to a dated subfolder under here.
DIGEST_DIR = REPO_ROOT / "_digest"
FEEDS_FILE = HERE / "feeds.txt"
CORE_FEEDS_FILE = HERE / "feeds-core.txt"   # small, trusted subset for fallback
STATE_DIR = HERE / "state"
SEEN_FILE = STATE_DIR / "seen.json"
RUN_LOG = STATE_DIR / "run.log"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Some feeds stamp dates with non-standard zone abbreviations; map them so
# dateutil doesn't warn/fail (UT and GMT are effectively UTC).
TZINFOS = {"UT": dt.timezone.utc, "GMT": dt.timezone.utc, "UTC": dt.timezone.utc}

# Feed fetching: per-feed (connect, read) timeout so a slow/dead feed can't
# stall the whole run, and a UA since some feeds reject the default.
FETCH_TIMEOUT = (10, 20)
USER_AGENT = ("Mozilla/5.0 (compatible; rm-fr-digest/1.0; "
              "+https://rm-fr.dev/blog/)")

# Set by main(): when False, per-feed fetch failures are summarized, not listed.
VERBOSE = False


class _Tee:
    """Write to several streams at once (console + log file)."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            try:
                s.write(data)
                s.flush()
            except (ValueError, OSError):
                pass

    def flush(self):
        for s in self.streams:
            try:
                s.flush()
            except (ValueError, OSError):
                pass

# Maps the human-facing section name the model returns to the `section`
# front-matter slug used by the tab pages (Feed / Deep Dives).
SECTION_SLUGS = {"feed": "feed", "deep dives": "deep-dives"}
DEFAULT_SECTION = "feed"
VALID_SEVERITY = {"low", "medium", "high", "critical"}


def load_dotenv():
    """Minimal .env loader (only sets vars that aren't already in the env)."""
    env_path = HERE / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def cfg(name, default=None):
    # Treat an unset OR empty-string value (e.g. a GitHub Actions variable that
    # isn't set) as "use the default".
    val = os.environ.get(name)
    return val if val not in (None, "") else default


def _scrub(text):
    """Strip API keys from a string before it is logged."""
    text = str(text)
    for var in ("GEMINI_API_KEY", "OPENROUTER_API_KEY"):
        val = os.environ.get(var)
        if val:
            text = text.replace(val, "***REDACTED***")
    # Also redact any leftover `?key=` / `&key=` query params just in case.
    text = re.sub(r"([?&]key=)[^\s&]+", r"\1***REDACTED***", text)
    return text


# ----------------------------------------------------------------------------
# Feed fetching
# ----------------------------------------------------------------------------
def read_feeds(path=FEEDS_FILE):
    urls = []
    if not Path(path).exists():
        return urls
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            urls.append(line)
    return urls


def entry_id(entry):
    raw = entry.get("id") or entry.get("link") or entry.get("title", "")
    return hashlib.sha1(raw.strip().lower().encode("utf-8")).hexdigest()


def entry_datetime(entry):
    for key in ("published", "updated", "created"):
        val = entry.get(key)
        if val:
            try:
                d = dateparser.parse(val, tzinfos=TZINFOS)
                if d.tzinfo is None:
                    d = d.replace(tzinfo=dt.timezone.utc)
                return d.astimezone(dt.timezone.utc)
            except (ValueError, OverflowError, TypeError):
                pass
    return None


def clean_text(html, limit=600):
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


_HOST_GUARD = threading.Lock()
_host_mutex = {}     # host -> Lock (serialize requests to the same host)
_host_last = {}      # host -> last request time (space them out)


def _host_lock(host):
    with _HOST_GUARD:
        return _host_mutex.setdefault(host, threading.Lock())


def _fetch_feed(url):
    """Fetch + parse one feed. Returns (url, parsed|Exception).

    Requests to the same host are serialized and spaced by DIGEST_HOST_GAP
    seconds so that hosts carrying many feeds (e.g. medium.com) don't see a
    burst and rate-limit us. A single retry covers transient 429/503/network
    blips.
    """
    host = urlparse(url).netloc.lower()
    gap = float(cfg("DIGEST_HOST_GAP", "0.8"))
    lock = _host_lock(host)
    err = None
    for attempt in range(2):
        resp = None
        with lock:
            wait = gap - (time.monotonic() - _host_last.get(host, 0.0))
            if wait > 0:
                time.sleep(wait)
            try:
                resp = requests.get(url, timeout=FETCH_TIMEOUT,
                                    headers={"User-Agent": USER_AGENT})
            except Exception as exc:  # noqa: BLE001
                err = exc
            finally:
                _host_last[host] = time.monotonic()
        if resp is None:
            if attempt == 0:
                time.sleep(2)
                continue
            return url, err
        if resp.status_code in (429, 503) and attempt == 0:
            time.sleep(5)
            continue
        try:
            resp.raise_for_status()
            return url, feedparser.parse(resp.content)
        except Exception as exc:  # noqa: BLE001
            return url, exc
    return url, (err or RuntimeError("retry exhausted"))


def collect_candidates(feeds, seen, lookback_hours, max_candidates, core_urls=None):
    core_urls = core_urls or set()
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=lookback_hours)
    workers = max(1, int(cfg("DIGEST_FETCH_WORKERS", "24")))

    # Fetch all feeds concurrently — this is the slow part otherwise.
    print(f"  fetching concurrently ({workers} workers)...")
    results, failures = [], 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        for url, parsed in ex.map(_fetch_feed, feeds):
            if isinstance(parsed, Exception):
                failures += 1
                if VERBOSE:
                    print(f"  ! skip {url}: {_scrub(parsed)}", file=sys.stderr)
            else:
                results.append((url, parsed))
    if failures:
        print(f"  ({failures} feed(s) unreachable, skipped"
              f"{'' if VERBOSE else '; run with --verbose to list them'})")

    candidates = []
    for url, parsed in results:
        source = parsed.feed.get("title", url)
        is_core = url in core_urls
        for entry in parsed.entries:
            eid = entry_id(entry)
            if eid in seen:
                continue
            when = entry_datetime(entry)
            if when is None or when < cutoff:
                continue
            candidates.append({
                "id": eid,
                "title": entry.get("title", "").strip(),
                "link": entry.get("link", "").strip(),
                "source": source,
                "published": when.isoformat(),
                "summary": clean_text(entry.get("summary", "")),
                "core": is_core,
            })
    # newest first, then cap
    candidates.sort(key=lambda c: c["published"], reverse=True)
    return candidates[:max_candidates]


# ----------------------------------------------------------------------------
# LLM curation
# ----------------------------------------------------------------------------
CURATE_SYSTEM = (
    "You are the editor of a security + AI intelligence digest. You receive a "
    "list of candidate news items pulled from RSS feeds. Select only the items "
    "that genuinely matter to a security engineer or offensive-security "
    "practitioner: new CVEs and exploits, breaches, malware/threat-actor "
    "activity, notable tooling/research, and major AI developments with security "
    "relevance. Aggressively drop marketing, low-value, or off-topic items. "
    "CRITICAL — DE-DUPLICATE: many feeds carry the SAME underlying story. If two "
    "or more candidates describe the same event, vulnerability, breach, or "
    "report, output it only ONCE, choosing the single most authoritative/complete "
    "source and discarding the rest. Never emit two items about the same story. "
    "For each selected item, rewrite the headline cleanly and write a concise "
    "3-6 sentence summary in your own words."
)


def curate_prompt(candidates, max_publish):
    listing = []
    for i, c in enumerate(candidates):
        listing.append(
            f"[{i}] TITLE: {c['title']}\n"
            f"    SOURCE: {c['source']}\n"
            f"    SNIPPET: {c['summary']}\n"
            f"    URL: {c['link']}"
        )
    items_block = "\n\n".join(listing)
    return (
        f"Here are {len(candidates)} candidate items. First merge duplicates "
        f"(the same story from different outlets is ONE item), then select the "
        f"most important. HARD LIMIT: return NO MORE THAN {max_publish} objects "
        f"total — never exceed {max_publish}.\n\n"
        f"{items_block}\n\n"
        "Return ONLY a JSON array (no prose, no code fences). Each element:\n"
        "{\n"
        '  "index": <int, the [n] of the source item>,\n'
        '  "title": "<rewritten clean headline>",\n'
        '  "summary": "<3-6 sentence summary in your own words>",\n'
        '  "section": "Feed" | "Deep Dives",  '
        "// Deep Dives only for deep technical analysis/long reads\n"
        '  "severity": "low" | "medium" | "high" | "critical",\n'
        '  "tags": ["lowercase-hyphenated", "max-4"],\n'
        '  "must_know": true | false  // true for AT MOST 3-5 of the single most '
        "critical items in the whole batch; default false. Most items are false.\n"
        "}\n"
        "If nothing is worth publishing, return []."
    )


def extract_json_array(text):
    """Pull the first JSON array out of a model response, tolerating fences/prose."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass
    return None


def call_openrouter(candidates, max_publish):
    api_key = cfg("OPENROUTER_API_KEY")
    if not api_key:
        return None
    model = cfg("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if cfg("OPENROUTER_SITE_URL"):
        headers["HTTP-Referer"] = cfg("OPENROUTER_SITE_URL")
    if cfg("OPENROUTER_APP_NAME"):
        headers["X-Title"] = cfg("OPENROUTER_APP_NAME")
    payload = {
        "model": model,
        "temperature": 0.3,
        "messages": [
            {"role": "system", "content": CURATE_SYSTEM},
            {"role": "user", "content": curate_prompt(candidates, max_publish)},
        ],
    }
    last_err = None
    for attempt in range(3):
        try:
            resp = requests.post(OPENROUTER_URL, headers=headers,
                                 json=payload, timeout=120)
            if resp.status_code in (429, 500, 502, 503, 504):
                wait = 8 * (attempt + 1)
                print(f"  openrouter busy ({resp.status_code}), "
                      f"retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
            parsed = extract_json_array(content)
            if parsed is None:
                last_err = "could not parse JSON from model output"
                print(f"  ! {last_err}; retrying...", file=sys.stderr)
                continue
            return parsed
        except (requests.RequestException, KeyError, ValueError) as exc:
            last_err = _scrub(exc)
            print(f"  ! OpenRouter error: {last_err}", file=sys.stderr)
            time.sleep(4 * (attempt + 1))
    print(f"  ! giving up on LLM curation: {last_err}", file=sys.stderr)
    return None


def call_gemini(candidates, max_publish):
    """Curate via Google Gemini (free tier through Google AI Studio)."""
    api_key = cfg("GEMINI_API_KEY")
    if not api_key:
        return None
    model = cfg("GEMINI_MODEL", "gemini-2.5-flash")
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{model}:generateContent")
    # Key goes in a header (never the URL) so it can't leak into logs/errors.
    headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}
    gen_config = {
        "temperature": 0.3,
        "responseMimeType": "application/json",
        # Max length of the model's reply (not a billing/quota limit; free
        # models stay free). Big enough that the JSON never truncates.
        "maxOutputTokens": int(cfg("GEMINI_MAX_OUTPUT_TOKENS", "16384")),
    }
    # 2.5 models "think" by default, which is slow and unnecessary for curation
    # and is the usual cause of read timeouts on the free tier. Turn it off.
    if "2.5" in model:
        gen_config["thinkingConfig"] = {"thinkingBudget": 0}
    body = {
        "system_instruction": {"parts": [{"text": CURATE_SYSTEM}]},
        "contents": [
            {"role": "user",
             "parts": [{"text": curate_prompt(candidates, max_publish)}]},
        ],
        "generationConfig": gen_config,
    }
    last_err = None
    for attempt in range(4):
        try:
            resp = requests.post(url, headers=headers, json=body, timeout=180)
            # 429 = rate limit; 5xx = transient overload -> back off and retry.
            if resp.status_code in (429, 500, 502, 503, 504):
                wait = 8 * (attempt + 1)
                print(f"  gemini busy ({resp.status_code}), retrying in {wait}s...",
                      file=sys.stderr)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            content = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = extract_json_array(content)
            if parsed is None:
                last_err = "could not parse JSON from Gemini output"
                print(f"  ! {last_err}; retrying...", file=sys.stderr)
                continue
            return parsed
        except (requests.RequestException, KeyError, IndexError, ValueError) as exc:
            last_err = _scrub(exc)
            print(f"  ! Gemini error: {last_err}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    print(f"  ! giving up on Gemini: {last_err}", file=sys.stderr)
    return None


def _provider_candidates(name, candidates):
    """Pick the candidate slice a provider should curate over.

    OpenRouter's free models have a small context window and tight rate
    limits, so it only sees the trusted 'core' feeds (feeds-core.txt),
    capped to OPENROUTER_MAX_CANDIDATES. Gemini (large context) sees the
    full list.
    """
    if name == "openrouter":
        core = [c for c in candidates if c.get("core")]
        pool = core or candidates
        cap = int(cfg("OPENROUTER_MAX_CANDIDATES", "40"))
        return pool[:cap]
    return candidates


def call_llm(candidates, max_publish):
    """Try the primary provider, then the other as a fallback.

    Returns a list of normalized, ready-to-write items, or None if every
    provider with a key failed (so the caller can avoid publishing junk and
    can retry the same items next run).
    """
    providers = {"gemini": call_gemini, "openrouter": call_openrouter}
    keyed = {
        "gemini": bool(cfg("GEMINI_API_KEY")),
        "openrouter": bool(cfg("OPENROUTER_API_KEY")),
    }
    if not any(keyed.values()):
        print("  no LLM key found in environment "
              "(checked GEMINI_API_KEY, OPENROUTER_API_KEY)", file=sys.stderr)
        return None
    print(f"  providers with keys: "
          f"{', '.join(n for n, ok in keyed.items() if ok)}")
    primary = cfg("LLM_PRIMARY", "gemini").strip().lower()
    if primary not in providers:
        primary = "gemini"
    order = [primary] + [p for p in providers if p != primary]
    for name in order:
        if not keyed[name]:
            continue
        subset = _provider_candidates(name, candidates)
        print(f"  trying {name} over {len(subset)} candidate(s)...")
        raw = providers[name](subset, max_publish)
        if raw is not None:
            items = normalize_selection(raw, subset)
            print(f"  curated via {name}: {len(items)} item(s)")
            return items
    return None


def normalize_selection(selection, candidates):
    """Validate model output and merge it back with source metadata."""
    out = []
    for item in selection:
        try:
            idx = int(item["index"])
        except (KeyError, ValueError, TypeError):
            continue
        if idx < 0 or idx >= len(candidates):
            continue
        src = candidates[idx]
        section = SECTION_SLUGS.get(
            str(item.get("section", "")).strip().lower(), DEFAULT_SECTION)
        severity = str(item.get("severity", "medium")).lower()
        if severity not in VALID_SEVERITY:
            severity = "medium"
        tags = [slugify(t) for t in item.get("tags", []) if str(t).strip()][:4]
        out.append({
            "title": item.get("title") or src["title"],
            "summary": item.get("summary") or src["summary"],
            "section": section,
            "severity": severity,
            "tags": tags or ["security"],
            "must_know": bool(item.get("must_know", False)),
            "source": src["source"],
            "link": src["link"],
            "published": src["published"],
        })
    return out


# Generic words that shouldn't drive similarity (every security headline has them).
_DEDUPE_STOP = {
    "the", "a", "an", "to", "of", "in", "for", "and", "on", "with", "via", "is",
    "are", "as", "at", "by", "from", "into", "could", "have", "has", "new",
    "attack", "attacks", "flaw", "flaws", "vulnerability", "vulnerabilities",
    "bug", "bugs", "exploit", "exploited", "allows", "allow", "lets", "let",
    "used", "critical", "released", "update", "updated", "warns", "warning",
}
_CVE_RE = re.compile(r"cve-\d{4}-\d{4,7}", re.IGNORECASE)


def _title_tokens(title):
    toks = set(re.findall(r"[a-z0-9]+", (title or "").lower()))
    return {t for t in toks if t not in _DEDUPE_STOP and len(t) > 1}


def _cve_ids(item):
    text = f"{item.get('title', '')} {item.get('summary', '')}".lower()
    return set(_CVE_RE.findall(text))


def _dedupe_items(items, threshold=0.45):
    """Drop near-duplicate stories. A safety net over the model's own de-dup:
    many feeds carry the same story and the model sometimes emits 2-3 variants.

    Two signals: a shared CVE id (strong), or high title-token overlap (Jaccard).
    """
    kept, kept_tokens, kept_cves = [], [], []
    for it in items:
        toks = _title_tokens(it.get("title", ""))
        cves = _cve_ids(it)
        dup = (cves and any(cves & kc for kc in kept_cves)) or (
            toks and any(
                kt and len(toks & kt) / len(toks | kt) >= threshold
                for kt in kept_tokens
            )
        )
        if dup:
            continue
        kept.append(it)
        kept_tokens.append(toks)
        kept_cves.append(cves)
    return kept


_SEV_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def _cap_must_know(items, cap):
    """Keep must_know on only the top `cap` items (by severity); demote the rest.

    Top Picks should be the few highest-impact stories, not most of the feed.
    """
    flagged = [it for it in items if it.get("must_know")]
    if len(flagged) <= cap:
        return items
    flagged.sort(key=lambda it: _SEV_RANK.get(it.get("severity", "low"), 9))
    keep = {id(it) for it in flagged[:cap]}
    for it in items:
        if it.get("must_know") and id(it) not in keep:
            it["must_know"] = False
    return items


def raw_fallback(candidates, max_publish):
    """No-LLM mode: publish newest items as plain link posts."""
    out = []
    for c in candidates[:max_publish]:
        out.append({
            "title": c["title"],
            "summary": c["summary"] or "(no summary provided by source)",
            "section": DEFAULT_SECTION,
            "severity": "medium",
            "tags": ["security"],
            "must_know": False,
            "source": c["source"],
            "link": c["link"],
            "published": c["published"],
        })
    return out


# ----------------------------------------------------------------------------
# Post writing
# ----------------------------------------------------------------------------
def slugify(text):
    text = re.sub(r"[^\w\s-]", "", (text or "").lower())
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:70] or "item"


SEVERITY_PROMPT = {
    "critical": "prompt-danger",
    "high": "prompt-warning",
    "medium": "prompt-info",
    "low": "prompt-tip",
}


def yaml_escape(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_post(item, out_dir, dry_run=False):
    published = dateparser.parse(item["published"]).astimezone(dt.timezone.utc)
    fm_date = published.strftime("%Y-%m-%d %H:%M:%S +0000")
    slug = slugify(item["title"])
    path = out_dir / f"{slug}.md"
    n = 2
    while path.exists():
        path = out_dir / f"{slug}-{n}.md"
        n += 1

    tags = ", ".join(item["tags"])
    fm = [
        "---",
        f"title: {yaml_escape(item['title'])}",
        f"date: {fm_date}",
        f"section: {item['section']}",
        f"tags: [{tags}]",
        f"severity: {item['severity']}",
        f"must_know: {'true' if item['must_know'] else 'false'}",
        "sources:",
        f"  - title: {yaml_escape(item['source'])}",
        f"    url: {yaml_escape(item['link'])}",
        "---",
        "",
    ]
    # Body is just the summary; the digest layout renders the severity pill,
    # date, tags, and sources from front matter.
    content = "\n".join(fm) + item["summary"] + "\n"

    if dry_run:
        print(f"  [dry-run] would write {path.name}  "
              f"({item['section']} / {item['severity']}"
              f"{' / MUST-KNOW' if item['must_know'] else ''})")
        return None
    out_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  + {path.name}  ({item['section']} / {item['severity']}"
          f"{' / MUST-KNOW' if item['must_know'] else ''})")
    return path


# ----------------------------------------------------------------------------
# State
# ----------------------------------------------------------------------------
def load_seen():
    if not SEEN_FILE.exists():
        return {}
    try:
        return json.loads(SEEN_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_seen(seen):
    # Prune entries older than 60 days to keep the file small.
    cutoff = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=60)).isoformat()
    pruned = {k: v for k, v in seen.items() if v >= cutoff}
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    SEEN_FILE.write_text(json.dumps(pruned, indent=0, sort_keys=True),
                         encoding="utf-8")


# ----------------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------------
def _start_logging(dry_run):
    """Tee stdout/stderr to state/run.log with a timestamped header."""
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        # Keep the log from growing without bound: trim to the recent ~500 KB.
        if RUN_LOG.exists() and RUN_LOG.stat().st_size > 1_000_000:
            tail = RUN_LOG.read_text(encoding="utf-8", errors="replace")[-500_000:]
            RUN_LOG.write_text(tail, encoding="utf-8")
        logf = open(RUN_LOG, "a", encoding="utf-8")
        logf.write(f"\n===== {dt.datetime.now(dt.timezone.utc).isoformat()} "
                   f"(dry_run={dry_run}) =====\n")
        sys.stdout = _Tee(sys.__stdout__, logf)
        sys.stderr = _Tee(sys.__stderr__, logf)
    except OSError as exc:
        print(f"  ! could not open run log: {exc}", file=sys.stderr)


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Build the security/AI digest.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Don't write posts or update state; just report.")
    ap.add_argument("--verbose", action="store_true",
                    help="List every unreachable feed (otherwise just a count).")
    args = ap.parse_args()

    load_dotenv()
    global VERBOSE
    VERBOSE = args.verbose or cfg("DIGEST_VERBOSE", "").strip().lower() \
        in ("1", "true", "yes")
    _start_logging(args.dry_run)

    # Weekly cadence: look back ~7.5 days so nothing slips between runs.
    lookback = int(cfg("DIGEST_LOOKBACK_HOURS", "180"))
    max_candidates = int(cfg("DIGEST_MAX_CANDIDATES", "120"))
    max_publish = int(cfg("DIGEST_MAX_PUBLISH", "20"))

    feeds = read_feeds()
    core_urls = set(read_feeds(CORE_FEEDS_FILE))
    seen = load_seen()
    now_iso = dt.datetime.now(dt.timezone.utc).isoformat()

    print(f"Reading {len(feeds)} feeds "
          f"({len(core_urls)} core; lookback {lookback}h)...")
    candidates = collect_candidates(feeds, seen, lookback, max_candidates,
                                    core_urls)
    print(f"Found {len(candidates)} new candidate items.")
    if not candidates:
        print("Nothing new. Done.")
        return

    items = call_llm(candidates, max_publish)
    curation_failed = items is None
    if curation_failed:
        allow_raw = cfg("DIGEST_ALLOW_RAW_FALLBACK", "false").strip().lower() \
            in ("1", "true", "yes")
        if allow_raw:
            items = raw_fallback(candidates, max_publish)
            curation_failed = False
            print(f"LLM unavailable — raw fallback selected {len(items)} item(s).")
        else:
            items = []
            print("LLM unavailable; raw fallback disabled, so publishing NOTHING "
                  "this run (no junk). These items will be retried next run. "
                  "Set DIGEST_ALLOW_RAW_FALLBACK=true to override.")

    # Enforce de-duplication, the publish cap, and the Top Picks cap in code —
    # never trust the model to respect any of them on its own.
    if items:
        n0 = len(items)
        items = _dedupe_items(items)[:max_publish]
        max_mk = int(cfg("DIGEST_MAX_MUST_KNOW", "5"))
        items = _cap_must_know(items, max_mk)
        mk = sum(1 for it in items if it.get("must_know"))
        note = f" (trimmed from {n0} by dedupe/cap)" if len(items) != n0 else ""
        print(f"Publishing {len(items)} item(s), {mk} flagged Top Pick{note}.")

    # Each run writes into its own dated subfolder of the digest collection.
    run_dir = DIGEST_DIR / dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

    written = 0
    for item in items:
        if write_post(item, run_dir, dry_run=args.dry_run):
            written += 1

    if args.dry_run:
        print("[dry-run] state not modified.")
        return

    # Only advance state if curation actually ran. If every provider failed,
    # leave the candidates unseen so the next run retries them.
    if curation_failed:
        print(f"Wrote {written} post(s); state NOT advanced (curation failed, "
              "items will be retried next run).")
    else:
        for c in candidates:
            seen[c["id"]] = now_iso
        save_seen(seen)
        print(f"Wrote {written} post(s); state updated ({len(seen)} ids tracked).")


if __name__ == "__main__":
    main()
