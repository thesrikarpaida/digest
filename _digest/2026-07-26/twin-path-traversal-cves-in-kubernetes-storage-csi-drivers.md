---
title: "Twin Path Traversal CVEs in Kubernetes Storage CSI Drivers"
date: 2026-07-23 13:00:50 +0000
section: feed
tags: [kubernetes, cve, cloud-security, vulnerability]
severity: high
must_know: false
sources:
  - title: "SentinelOne"
    url: "https://www.sentinelone.com/blog/mount-here-read-there-twin-path-traversal-cves-in-kubernetes-storage/"
---
SentinelOne researchers discovered two path traversal vulnerabilities in Kubernetes Container Storage Interface (CSI) drivers, stemming from a misconception in `filepath.Join` usage. These flaws could allow cross-tenant path traversal, enabling attackers to access or manipulate data outside their intended storage boundaries. This highlights a critical security risk in multi-tenant Kubernetes environments and the complexities of secure file path handling.
