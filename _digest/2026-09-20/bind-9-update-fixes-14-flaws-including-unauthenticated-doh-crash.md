---
title: "BIND 9 Update Fixes 14 Flaws, Including Unauthenticated DoH Crash"
date: 2026-09-17 08:00:29 +0000
section: feed
tags: [bind9, dns, dos, vulnerability]
severity: high
must_know: false
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/09/bind-9-update-fixes-14-flaws-including.html"
---
The Internet Systems Consortium (ISC) has released BIND 9.20.29 and 9.21.26 to address fourteen security flaws. One critical vulnerability affects any BIND server answering DNS-over-HTTPS (DoH), allowing an unauthenticated sender to crash the 'named' process with a single invalid request. All BIND 9 users are advised to update to the latest versions to mitigate these risks.
