---
title: "Bing Images Flaws Allowed RCE as SYSTEM on Microsoft Servers"
date: 2026-07-24 11:45:17 +0000
section: feed
tags: [rce, microsoft, vulnerability, svg]
severity: critical
must_know: true
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/07/bing-images-flaws-let-crafted-svgs-run.html"
---
Researchers discovered critical vulnerabilities (CVE-2026-32194 and CVE-2026-32195) in Bing's image search that allowed crafted SVG files to execute commands as NT AUTHORITY\SYSTEM on Microsoft's production image-processing workers. The same flaws also granted root access on Linux machines within the same fleet. These issues were found across various hosts and network ranges, indicating a systemic problem within Bing's image tier.
