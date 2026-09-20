---
title: "Critical Docker Sandboxes Flaw Allows macOS Host File Access"
date: 2026-09-17 15:37:56 +0000
section: feed
tags: [docker, macos, sandbox-escape, privilege-escalation]
severity: critical
must_know: true
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/09/critical-docker-sandboxes-flaw-lets.html"
---
Docker has disclosed a critical vulnerability, CVE-2026-77179, in Docker Sandboxes for macOS. This flaw allows malicious code running within a Docker Sandboxes virtual machine to escape its shared project directory and read or modify files anywhere on the macOS host. The escape operates with the privileges of the host user running the VM, affecting versions prior to 27.0.0. Organizations should update to Parallels Desktop 27 to address this issue.
