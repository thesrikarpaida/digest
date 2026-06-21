---
title: "Microsoft Surface Devices Vulnerable to Local Privilege Escalation"
date: 2026-06-20 21:01:50 +0000
section: feed
tags: [privilege-escalation, microsoft-surface, windows]
severity: critical
must_know: true
sources:
  - title: "The Contractor"
    url: "https://thecontractor.io/ms-surface-eop-system/"
---
A critical vulnerability in Microsoft's Surface Device Management Architecture allows a standard user to escalate privileges to NT AUTHORITY\SYSTEM. This exploit requires no administrative prerequisites, UAC bypass, or user interaction, making it a significant threat for any Surface device. The attack chain involves two authorization failures and can be completed in eight steps, followed by a reboot.
