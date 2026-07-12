---
title: "Compromised jscrambler npm Package Drops Rust Infostealer"
date: 2026-07-11 17:59:26 +0000
section: feed
tags: [supply-chain, malware, npm, infostealer]
severity: critical
must_know: true
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/07/compromised-jscrambler-8140-npm-release.html"
---
The jscrambler npm package, version 8.14.0, was compromised to deliver a Rust-based infostealer. Installing this malicious version executes a preinstall hook that drops and runs a native binary tailored for Windows, macOS, or Linux. The compromise was quickly detected, highlighting the ongoing supply chain risks in software development.
