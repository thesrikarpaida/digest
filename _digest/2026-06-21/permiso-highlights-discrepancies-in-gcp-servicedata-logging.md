---
title: "Permiso Highlights Discrepancies in GCP serviceData Logging"
date: 2026-06-16 12:46:59 +0000
section: deep-dives
tags: [gcp, cloud-security, logging, detection-engineering]
severity: medium
must_know: false
sources:
  - title: "Cloud Chronicles"
    url: "https://permiso.io/blog/gcp-servicedata-officially-deprecated-actively-dangerous"
---
Permiso has published research highlighting discrepancies in Google Cloud Platform (GCP) audit logs, specifically concerning `serviceData` in Logs Explorer versus exported logs. Cloud audit logs are crucial for detection engineering and incident response, providing telemetry for identifying suspicious behavior. The quality and completeness of these traces directly impact the reliability of security efforts, and inconsistencies can hinder effective threat detection and investigation in GCP environments.
