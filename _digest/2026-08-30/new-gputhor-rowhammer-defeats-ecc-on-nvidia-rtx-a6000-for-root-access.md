---
title: "New GPUThor Rowhammer Defeats ECC on NVIDIA RTX A6000 for Root Access"
date: 2026-08-27 08:13:11 +0000
section: deep-dives
tags: [hardware-security, gpu, rowhammer, privilege-escalation]
severity: critical
must_know: false
sources:
  - title: "The Hacker News"
    url: "https://thehackernews.com/2026/08/gputhor-rowhammer-defeats-ecc-on-nvidia.html"
---
Academic researchers have developed GPUThor, a Rowhammer attack that impacts NVIDIA workstation GPUs with GDDR6 memory, including the RTX A6000. This attack successfully defeats error correction codes (ECC), a recommended mitigation, to achieve denial-of-service (DoS) and privilege escalation to a root shell. GPUThor demonstrates a significant hardware-level vulnerability with implications for GPU-accelerated computing environments.
