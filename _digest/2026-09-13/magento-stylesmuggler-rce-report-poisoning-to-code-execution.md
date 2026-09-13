---
title: "Magento StyleSmuggler RCE: Report Poisoning to Code Execution"
date: 2026-09-12 15:18:37 +0000
section: deep-dives
tags: [magento, rce, vulnerability, exploit]
severity: critical
must_know: false
sources:
  - title: "FORTBRIDGE"
    url: "https://fortbridge.co.uk/research/stylesmuggler-magento-unauthenticated-rce/"
---
FORTBRIDGE researchers have detailed a complete HTTP-only reconstruction of the StyleSmuggler vulnerability (CVE-2026-75650) in Magento. This unauthenticated remote code execution chain involves report poisoning and a guest billing-address parser flaw, leading through Email Preview, AWS S3Client, and ArrayScanner to final PHP include. A working lab PoC and analysis of Adobe's hotfix are provided, offering deep insight into this critical flaw.
