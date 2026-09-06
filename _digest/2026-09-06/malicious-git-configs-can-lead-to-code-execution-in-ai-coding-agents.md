---
title: "Malicious .git Configs Can Lead to Code Execution in AI Coding Agents"
date: 2026-09-02 14:06:59 +0000
section: feed
tags: [ai-security, supply-chain, code-execution, git]
severity: high
must_know: false
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/09/malicious-git-configs-can-make-claude.html"
---
Manifold Security has uncovered eight security flaws across seven command-line AI coding agents, including Claude, Codex, and Cursor. These vulnerabilities stem from malicious Git configurations that can name a command, which the agent then executes on the developer's machine without a sandbox or approval prompt. Exploitation requires the repository to be cloned, posing a supply chain risk for developers using these AI tools.
