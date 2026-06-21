---
title: "Google Vertex AI SDK Flaw Allows Cross-Tenant RCE via Bucket Squatting"
date: 2026-06-16 19:05:41 +0000
section: feed
tags: [google-cloud, ai-security, rce, vulnerability]
severity: critical
must_know: true
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/06/google-vertex-ai-sdk-flaw-let-attackers.html"
---
Palo Alto Networks Unit 42 discovered a critical vulnerability, dubbed 'Pickle in the Middle,' in the Google Cloud Vertex AI SDK for Python. This flaw could allow an attacker, without any access to a victim's project, to hijack machine learning model uploads and execute code within Google's serving infrastructure. The attack leverages 'bucket squatting' to achieve cross-tenant remote code execution. Google has patched the vulnerability, and no in-the-wild exploitation was observed.
