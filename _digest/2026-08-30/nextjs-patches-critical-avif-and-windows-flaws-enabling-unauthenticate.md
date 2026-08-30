---
title: "Next.js Patches Critical AVIF and Windows Flaws Enabling Unauthenticated RCE"
date: 2026-08-27 15:13:00 +0000
section: feed
tags: [nextjs, rce, cve, web-framework]
severity: critical
must_know: false
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/08/nextjs-patches-critical-avif-and.html"
---
Vercel has released security patches for two critical vulnerabilities in the Next.js web framework, both allowing unauthenticated remote code execution. CVE-2026-75604, a path traversal flaw, affects Windows filesystems, while another is exploitable via specially crafted AVIF image files. Developers using Next.js should update immediately to prevent server compromise.
