---
title: "Frida 17.15.0 Released with Threading and Function Range Improvements"
date: 2026-06-19 10:38:42 +0000
section: feed
tags: [tooling, dynamic-analysis, frida]
severity: low
must_know: false
sources:
  - title: "Frida • A world-class dynamic instrumentation toolkit"
    url: "https://frida.re/news/2026/06/19/frida-17-15-0-released/"
---
Frida, the dynamic instrumentation toolkit, has released version 17.15.0, introducing several key improvements. Notable additions include `Process.getThreadById()` and `Process.findThreadById()` for efficient thread lookup, and `Process.getFunctionRange()` for convenient function range retrieval. The update also addresses a critical thread enumeration deadlock when a thread observer is attached, enhancing stability and reliability for dynamic analysis.
