---
title: "Claude Code and Gemini CLI Flaws Allow GitHub Issue to Reach CI Workflow Secrets"
date: 2026-08-07 08:18:35 +0000
section: feed
tags: [ai-security, cicd, github, prompt-injection]
severity: high
must_know: false
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/08/claude-code-and-gemini-cli-flaws-let.html"
---
Security flaws in Anthropic's and Google's coding-agent repositories allowed a GitHub issue, opened by an account with no repository privileges, to execute code on CI runners. For OpenAI, it was enough to hijack the next agent run. These vulnerabilities highlight risks in AI agent configurations and their interaction with CI/CD pipelines, potentially exposing workflow secrets.
