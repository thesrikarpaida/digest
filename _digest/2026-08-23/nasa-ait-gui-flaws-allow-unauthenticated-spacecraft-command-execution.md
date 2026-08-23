---
title: "NASA AIT-GUI Flaws Allow Unauthenticated Spacecraft Command Execution"
date: 2026-08-20 11:05:11 +0000
section: feed
tags: [nasa, spacecraft, rce, critical-infrastructure]
severity: critical
must_know: false
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/08/nasa-ait-gui-flaws-could-let.html"
---
Security researchers at Cycode have discovered a chain of flaws in NASA/JPL's open-source AMMOS Instrument Toolkit (AIT-GUI), a browser-based operator console. These vulnerabilities (GHSA-p9r8-2q67-fp86, CVSS 9.4) allow unauthenticated attackers to issue arbitrary commands to the software's spacecraft and instrument command bus. This represents a severe risk to space mission operations.
