---
title: "GhostPack Necromancy: Reforging C# Tools with WasmForge for EDR Evasion"
date: 2026-06-19 01:55:33 +0000
section: deep-dives
tags: [edr-evasion, red-team, wasm, tooling]
severity: medium
must_know: false
sources:
  - title: "Praetorian"
    url: "https://www.praetorian.com/blog/wasmforge-csharp-ghostpack-edr-evasion/"
---
Praetorian has introduced 'GhostPack Necromancy,' a technique for reforging C# tools using WasmForge to achieve opsec-safe binaries and evade EDR solutions. Building on their Go-to-WebAssembly loader, this approach extends to C# tools, many of which have become over-signatured by security products. By compiling these tools to WebAssembly, attackers can potentially bypass traditional endpoint detection mechanisms, offering a new avenue for red team operations and malware development.
