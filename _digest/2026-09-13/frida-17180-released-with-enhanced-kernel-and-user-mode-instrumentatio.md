---
title: "Frida 17.18.0 Released with Enhanced Kernel and User-Mode Instrumentation"
date: 2026-09-09 18:37:30 +0000
section: deep-dives
tags: [frida, reverse-engineering, instrumentation, tooling]
severity: low
must_know: false
sources:
  - title: "Frida • A world-class dynamic instrumentation toolkit"
    url: "https://frida.re/news/2026/09/09/frida-17-18-0-released/"
---
Frida 17.18.0 introduces significant advancements, particularly for its Barebone component. The XNU agent can now be loaded as a macOS kernel extension, and the Linux agent gains broader architecture support and access to kernel type information. The backend can instrument both kernel and user-mode processes across Linux, XNU, Windows NT, and even Windows 9x, making it a powerful tool for dynamic instrumentation and reverse engineering.
