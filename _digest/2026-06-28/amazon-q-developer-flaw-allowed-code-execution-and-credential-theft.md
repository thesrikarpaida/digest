---
title: "Amazon Q Developer Flaw Allowed Code Execution and Credential Theft"
date: 2026-06-26 13:53:00 +0000
section: feed
tags: [cve, cloud-security, ai-security, supply-chain]
severity: critical
must_know: true
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/06/amazon-q-developer-flaw-could-let.html"
---
A high-severity vulnerability (CVE-2026-12957, CVSS 8.5) in Amazon Q Developer allowed malicious repositories to execute arbitrary commands and steal cloud credentials. The flaw exploited how Amazon's AI coding assistant handled Model Context Protocol (MCP) servers. A developer merely opening and trusting a malicious workspace could lead to compromise. Amazon has since patched the vulnerability.
