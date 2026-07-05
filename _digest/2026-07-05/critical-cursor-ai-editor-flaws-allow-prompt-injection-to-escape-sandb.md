---
title: "Critical Cursor AI Editor Flaws Allow Prompt Injection to Escape Sandbox and Run Commands"
date: 2026-07-01 14:42:54 +0000
section: feed
tags: [ai, prompt-injection, rce, vulnerability]
severity: critical
must_know: true
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/07/critical-cursor-flaws-could-let-prompt.html"
---
Two critical vulnerabilities, CVE-2026-50548 and CVE-2026-50549 (CVSS 9.8/9.3), dubbed 'DuneSlide,' have been found in Cursor, an AI code editor. These flaws allow a seemingly innocuous prompt to bypass the editor's safety sandbox and execute arbitrary commands on a developer's machine without user interaction. This highlights a severe risk in AI-assisted development environments where prompt injection can lead to direct system compromise.
