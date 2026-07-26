---
title: "Nine-Year-Old RefluXFS Linux Flaw Gives Local Users Root on Default RHEL Installs"
date: 2026-07-23 08:04:35 +0000
section: feed
tags: [linux, privilege-escalation, cve, exploit]
severity: critical
must_know: false
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/07/nine-year-old-refluxfs-linux-flaw-gives.html"
---
A nine-year-old Linux kernel flaw, RefluXFS (CVE-2026-64600), has been disclosed, allowing unprivileged local users to gain persistent root access. This race condition in the XFS filesystem's copy-on-write path enables attackers to overwrite root-owned files. Qualys demonstrated its exploitability on default installations of Red Hat Enterprise Linux, Fedora Server, and Amazon Linux, even with SELinux in enforcing mode.
