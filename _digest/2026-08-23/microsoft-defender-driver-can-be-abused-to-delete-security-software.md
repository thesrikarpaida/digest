---
title: "Microsoft Defender Driver Can Be Abused to Delete Security Software"
date: 2026-08-21 15:52:10 +0000
section: feed
tags: [windows, privilege-escalation, edr-bypass, microsoft-defender]
severity: critical
must_know: true
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/08/microsoft-defenders-own-driver-can-be.html"
---
Check Point Research has uncovered a technique that weaponizes Microsoft Defender's legitimate boot-time remediation driver (BTR.sys) to perform arbitrary kernel-level file and registry operations. This allows attackers to delete security software at boot on Windows systems from Windows 7 to 11 25H2. The method exploits no software flaw and does not import external drivers, instead leveraging an existing, trusted component for malicious purposes.
