---
title: "Critical Next.js ImageResponse Flaw Allows Server Code Execution via Crafted SVG"
date: 2026-09-23 07:04:40 +0000
section: feed
tags: [nextjs, rce, web-vulnerability, svg]
severity: high
must_know: false
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/09/critical-nextjs-imageresponse-flaw-can.html"
---
Vercel has disclosed and patched a critical security vulnerability in Next.js that could lead to server-side code execution. The flaw, affecting the ImageResponse feature, allows attackers to run arbitrary code by injecting crafted SVG input when user-controlled values are used in image generation. Developers using Next.js are urged to update to version 14.2.4 or later to mitigate this risk.
