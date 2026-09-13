---
title: "Off Guard: Breaking LiteLLM from Authentication Bypass to Cloud Compromise"
date: 2026-09-09 16:06:00 +0000
section: deep-dives
tags: [ai, cloud-security, authentication-bypass, rce]
severity: critical
must_know: false
sources:
  - title: "Wiz Blog | RSS feed"
    url: "https://www.wiz.io/blog/off-guard-breaking-litellm-from-authentication-bypass-to-cloud-compromise"
---
Wiz Research details how misconfigurations in LiteLLM, an open-source AI gateway, can lead to cloud compromise. The report highlights that nearly one in ten internet-facing LiteLLM servers accepted the default 'sk-1234' admin key, allowing unauthenticated access. This vulnerability, combined with unauthenticated MCP sessions and custom code guardrails, exposes cloud AI infrastructure to root-level remote code execution and IAM theft.
