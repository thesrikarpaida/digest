---
title: "OS Command Injection in Splunk AI Toolkit Allows Admin RCE"
date: 2026-06-17 00:00:00 +0000
section: feed
tags: [cve, splunk, rce, ai-toolkit]
severity: critical
must_know: true
sources:
  - title: "Splunk Security Announcements"
    url: "https://advisory.splunk.com//advisories/SVD-2026-0614"
---
Splunk has disclosed a critical OS command injection vulnerability (SVD-2026-0614) in its AI Toolkit, affecting versions below 5.7.4. An authenticated user with the 'admin' Splunk role can execute arbitrary operating system commands on the host running Splunk Enterprise. This flaw stems from unsafe shell execution patterns in the `btool` configuration helper, which fails to properly sanitize dynamic parameters, allowing shell interpretation.
