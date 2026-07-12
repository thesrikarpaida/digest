---
title: "GhostApproval Symlink Flaws Allow Malicious Repos to Execute Code in AI Coding Assistants"
date: 2026-07-09 04:27:18 +0000
section: feed
tags: [ai-security, supply-chain, code-execution, ai-agents]
severity: critical
must_know: true
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/07/ghostapproval-symlink-flaws-could-let.html"
---
Wiz researchers discovered 'GhostApproval' flaws in six popular AI coding assistants, including Amazon Q Developer and Claude Code. This vulnerability allows a booby-trapped code project to gain control of a developer's machine. The attack works by tricking the assistant into requesting permission to edit a harmless file, but a symlink redirects the write operation to a sensitive system file, bypassing the human-in-the-loop safety model.
