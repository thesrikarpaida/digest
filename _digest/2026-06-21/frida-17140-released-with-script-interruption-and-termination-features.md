---
title: "Frida 17.14.0 Released with Script Interruption and Termination Features"
date: 2026-06-16 14:40:30 +0000
section: feed
tags: [tooling, frida, dynamic-analysis, reverse-engineering]
severity: low
must_know: false
sources:
  - title: "Frida • A world-class dynamic instrumentation toolkit"
    url: "https://frida.re/news/2026/06/16/frida-17-14-0-released/"
---
Frida, a dynamic instrumentation toolkit, has released version 17.14.0, focusing on improving control over runaway scripts. Key additions include `Script.interrupt()`, which aborts currently executing JavaScript while keeping the script loaded, and `Script.terminate()`, which interrupts execution and unloads the script. These features are particularly useful for REPLs and debugging, allowing developers and security researchers to recover from stuck evaluations and manage script lifecycles more effectively.
