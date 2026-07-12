---
title: "'Ghostcommit' Hides Prompt Injection in Images to Exfiltrate Secrets from AI Agents"
date: 2026-07-11 09:03:57 +0000
section: feed
tags: [ai-security, prompt-injection, data-exfiltration, ai-agents]
severity: high
must_know: true
sources:
  - title: "BleepingComputer"
    url: "https://www.bleepingcomputer.com/news/security/ghostcommit-hides-prompt-injection-in-images-to-fool-ai-agents-steal-secrets/"
---
Researchers have demonstrated 'Ghostcommit,' a technique that embeds prompt injection attacks within PNG images. This method successfully bypassed AI code reviewers like CodeRabbit and Bugbot, which do not process image files. The injected prompt then convinced a coding agent to read sensitive `.env` files and exfiltrate secrets, highlighting a novel vector for AI-driven data theft.
