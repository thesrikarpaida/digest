# Security + AI Digest

Automated daily intelligence feed for the blog, modeled on
[0day.digest](https://spbavarva.github.io/0day.digest/). It pulls a curated set
of offensive-security / AI RSS feeds, uses an LLM (Google Gemini by
default, with OpenRouter as a fallback) to filter the
noise and write short summaries, and publishes the result as Chirpy posts that
show up under the **FEED**, **DEEP DIVES**, and **TOP PICKS** tabs —
alongside your existing blog posts.

## How it fits together

```
feeds.txt ──► build_digest.py ──► _posts/*.md ──► Chirpy build ──► /blog
                   │                    ▲
                   ├─ OpenRouter (curate + summarize)
                   └─ state/seen.json (dedupe across runs)
```

- **Sections are set with a `section` field** (not categories). A post with
  `section: feed` shows on the FEED page; `section: deep-dives` shows on DEEP
  DIVES. Any post with `must_know: true` also appears on TOP PICKS. These tab
  pages live in `_tabs/`. (Categories are not used anywhere in this repo.)
- **Dedup state** lives in `state/seen.json` and is committed, so the scheduled
  job never reprocesses the same article.

## Running locally

```bash
cd tools/digest
cp .env.example .env          # then edit .env, add your OpenRouter key
pip install -r requirements.txt

python build_digest.py --dry-run   # see what it would publish
python build_digest.py             # actually write posts into ../../_posts
```

Then preview the site (from the repo root) with Docker:

```bash
docker compose up --build      # http://localhost:4000/blog/
```

## Providers & keys

The pipeline curates with an LLM. It tries a **primary** provider, and on any
failure falls back to the **secondary** one. Default order: **Gemini → OpenRouter**
(set `LLM_PRIMARY` to flip it). You only need a key for at least one.

You do **not** paste keys into any committed file.

- **Local:** put them in `tools/digest/.env` (git-ignored).
- **GitHub Actions:** add them as repository **secrets** under
  *Settings → Secrets and variables → Actions*:
  - `GEMINI_API_KEY` — free key from [Google AI Studio](https://aistudio.google.com/apikey)
  - `OPENROUTER_API_KEY` — optional fallback, from [OpenRouter](https://openrouter.ai/keys)

### Why Gemini by default

For a **weekly** run, each execution makes ~1 model call covering up to
`DIGEST_MAX_CANDIDATES` items in a single prompt. Gemini 2.5 Flash's large
context window fits that easily, and the free tier's per-day/per-minute limits
are nowhere near a once-a-week job — so it's effectively free here. OpenRouter
stays wired in as a no-effort fallback if Gemini errors or you hit a limit.

### Choosing models

- Gemini: `GEMINI_MODEL` (default `gemini-2.5-flash`; thinking is auto-disabled
  so it's fast). `gemini-2.5-flash-lite` is faster but follows the "max N + no
  duplicates" instructions less well, so prefer `flash`. `GEMINI_MAX_OUTPUT_TOKENS`
  (default 16384) caps reply length — not a billing limit.
- OpenRouter: `OPENROUTER_MODEL` (default `meta-llama/llama-3.3-70b-instruct:free`;
  other free options include `deepseek/deepseek-chat-v3-0324:free`).

The publish cap (`DIGEST_MAX_PUBLISH`) and de-duplication are enforced **in
code** after the model replies (title-similarity + shared-CVE), so a chatty or
sloppy model can't blow past the limit or emit the same story twice.

Set these locally in `.env`, or in CI as repository **variables**
(`GEMINI_MODEL`, `OPENROUTER_MODEL`, `LLM_PRIMARY`).

**If every provider fails (or no key is set), the script does not publish junk.**
By default it writes nothing that run and leaves those items unseen, so the next
run retries them — a transient Gemini `503` or OpenRouter `429` never costs you
items, and never dumps raw, un-curated posts onto the live site. Set
`DIGEST_ALLOW_RAW_FALLBACK=true` only if you want raw link posts (e.g. local
testing).

The fallback path is also lighter: OpenRouter curates over just the trusted
**core** feeds (`feeds-core.txt`), capped to `OPENROUTER_MAX_CANDIDATES`, since
its free models have a small context window and tight rate limits.

## Tuning (and where config lives)

Everything is configured with environment variables.

- **Locally:** put them in `tools/digest/.env` (see `.env.example`).
- **In the weekly GitHub Action:** `.env` is git-ignored and does **not** exist
  in CI. Set things under *Settings → Secrets and variables → Actions*:
  - **Secrets** tab → `GEMINI_API_KEY`, `OPENROUTER_API_KEY` (sensitive).
  - **Variables** tab → everything in the table below (non-sensitive). The
    workflow already passes all of them through, and any variable you leave
    unset falls back to the default — so you only set the ones you want to
    change. No need to edit the workflow file.

| Variable | Default | Meaning |
|----------|---------|---------|
| `LLM_PRIMARY` | `gemini` | Provider tried first (`gemini` or `openrouter`) |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Gemini model (`gemini-2.5-flash-lite` is faster) |
| `GEMINI_MAX_OUTPUT_TOKENS` | `16384` | Max length of Gemini's reply (not a billing limit) |
| `OPENROUTER_MODEL` | `meta-llama/llama-3.3-70b-instruct:free` | OpenRouter fallback model |
| `DIGEST_LOOKBACK_HOURS` | `180` | How far back a feed item counts as "new" (~7.5 days) |
| `DIGEST_MAX_CANDIDATES` | `120` | Items pulled before the model curates (Gemini) |
| `DIGEST_MAX_PUBLISH` | `20` | Max posts published per run |
| `DIGEST_MAX_MUST_KNOW` | `5` | Max items flagged Top Pick per run |
| `OPENROUTER_MAX_CANDIDATES` | `40` | Fallback only: cap on the core-feed slice sent to OpenRouter |
| `DIGEST_FETCH_WORKERS` | `24` | Feeds fetched in parallel (the slow step otherwise) |
| `DIGEST_HOST_GAP` | `0.8` | Min seconds between requests to the same host (avoids rate-limit cascades) |
| `DIGEST_ALLOW_RAW_FALLBACK` | `false` | If all LLMs fail, publish nothing (`false`) vs. raw link posts (`true`) |
| `DIGEST_VERBOSE` | `false` | List every unreachable feed vs. just a count (also `--verbose`) |

Edit `feeds.txt` to add/remove sources (one URL per line, `#` for comments).
It holds (near-)all of Graham Helton's list
(<https://grahamhelton.com/blog/rss-feeds>), with a high-signal "core" block at
the top. It is intentionally broad; the model curates the noise, and
`DIGEST_MAX_CANDIDATES` bounds each run. Trim the extended block if you want
less volume.

## Logs & state

- `tools/digest/state/run.log` — every run appends a timestamped block with all
  console output (git-ignored, auto-trimmed to ~500 KB). Check it to see what a
  past run did.
- `tools/digest/state/seen.json` — the dedupe ledger (committed). Only advances
  when curation actually succeeds.
- For the **weekly run on GitHub**, `run.log` is not committed — view the output
  in the repo's **Actions** tab instead:
  *Actions → "Weekly Digest" → pick the run → `generate-and-deploy` job →
  expand the "Generate digest" step.* (Logs are kept ~90 days; secret values
  are auto-masked as `***`.)

## Schedule

`.github/workflows/digest.yml` runs weekly on **Sundays at 08:00 UTC** (and
on-demand via *Actions → Weekly Digest → Run workflow*) — a low-traffic window
for the LLM APIs. Weekly keeps usage comfortably within the GitHub Actions free
quota. It generates posts, commits
them, then builds and deploys the site in the same job. Change the `cron:` line
to adjust timing.
