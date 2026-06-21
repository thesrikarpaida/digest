---
title: "Insecure Default Domain Allowlist in Splunk AI Toolkit Leads to Data Exfiltration"
date: 2026-06-17 00:00:00 +0000
section: feed
tags: [cve, splunk, data-exfiltration, ai-toolkit]
severity: high
must_know: false
sources:
  - title: "Splunk Security Announcements"
    url: "https://advisory.splunk.com//advisories/SVD-2026-0613"
---
Another vulnerability (SVD-2026-0613) has been found in Splunk AI Toolkit versions below 5.7.4, involving an insecure default domain allowlist. This flaw allows a low-privileged user, without 'admin' or 'power' roles, to force the AI Toolkit to make outbound HTTP requests to attacker-controlled servers. This could facilitate data exfiltration by bypassing intended domain restrictions for AI agent requests.
