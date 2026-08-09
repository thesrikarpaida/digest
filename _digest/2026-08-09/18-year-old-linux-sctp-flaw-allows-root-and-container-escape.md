---
title: "18-Year-Old Linux SCTP Flaw Allows Root and Container Escape"
date: 2026-08-07 11:10:33 +0000
section: feed
tags: [linux, container-escape, privilege-escalation, vulnerability]
severity: critical
must_know: true
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/08/18-year-old-linux-sctp-flaw-could-let.html"
---
A use-after-free bug in Linux's SCTP networking code, present since 2008, can be exploited to gain full root privileges on a host. Tencent researchers demonstrated its use to escape a container and access the underlying machine. Fixes have been released in stable kernels 7.1.6, 6.18.42, 6.12.101, and 6.6.148; users with older kernels and reachable SCTP should update immediately.
