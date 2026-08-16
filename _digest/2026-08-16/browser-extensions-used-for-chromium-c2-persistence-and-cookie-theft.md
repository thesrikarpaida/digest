---
title: "Browser Extensions Used for Chromium C2 Persistence and Cookie Theft"
date: 2026-08-13 16:00:00 +0000
section: deep-dives
tags: [browser-security, c2, persistence, cookie-theft]
severity: high
must_know: false
sources:
  - title: "SpecterOps"
    url: "https://specterops.io/blog/2026/08/13/chrome-devtools-protocol-cookie-theft/"
---
SpecterOps research reveals how browser extensions can be leveraged to turn Chromium into a persistent command and control (C2) platform. This method allows for silent installation of extensions, enabling continuous cookie theft and browser takeover. The technique builds on previous research into Chromium's Application Mode, highlighting a significant threat to authenticated browser sessions.
