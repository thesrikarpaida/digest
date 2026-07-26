---
title: "Chaos Ransomware Uses msaRAT to Route C2 Traffic Through Headless Browsers"
date: 2026-07-23 13:11:09 +0000
section: feed
tags: [ransomware, malware, c2, threat-actor]
severity: high
must_know: false
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/07/chaos-ransomware-uses-msarat-to-route.html"
---
The Chaos ransomware group is employing a new Rust-based implant, msaRAT, to route its command-and-control (C2) traffic through victims' own browsers. The malware launches Chrome or Edge in headless mode and drives the browser to communicate with the C2 server, never initiating outbound connections itself. This technique allows the ransomware to execute arbitrary commands while obscuring the attacker's IP address via WebRTC over TURN, making detection and attribution more challenging.
