---
title: "Unmasking SCCM Application Execution for Stealthier Detections"
date: 2026-09-10 16:00:00 +0000
section: deep-dives
tags: [sccm, detection, red-team, endpoint-security]
severity: medium
must_know: false
sources:
  - title: "SpecterOps"
    url: "https://specterops.io/blog/2026/09/10/unmasking-sccm-application-execution/"
---
SpecterOps research highlights that executing applications via SCCM's deploy application feature generates different artifacts compared to script-based execution, often evading existing detection tools. This post details how to detect these stealthier SCCM application execution methods. Understanding these differences is crucial for security teams to improve their detection capabilities against advanced persistent threats leveraging SCCM.
