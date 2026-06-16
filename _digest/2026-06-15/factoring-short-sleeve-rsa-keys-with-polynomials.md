---
title: "Factoring 'Short-Sleeve' RSA Keys with Polynomials"
date: 2026-06-12 11:00:00 +0000
section: deep-dives
tags: [cryptography, rsa, vulnerability, mathematics]
severity: high
must_know: false
sources:
  - title: "The Trail of Bits Blog"
    url: "https://blog.trailofbits.com/2026/06/12/factoring-short-sleeve-rsa-keys-with-polynomials/"
---
> **Severity: HIGH**
{: .prompt-warning }

Trail of Bits, in collaboration with Hanno Böck of the badkeys project, discovered a method to factor RSA private keys with heavily biased bits. These 'short-sleeve' keys, where bits are disproportionately zero, can be detected in the wild and quickly factored using a polynomial-based cryptanalysis technique. The research also identified the underlying bug responsible for generating these weak keys and tracked its historical impact, highlighting a significant cryptographic vulnerability.

**Source:** [The Trail of Bits Blog](https://blog.trailofbits.com/2026/06/12/factoring-short-sleeve-rsa-keys-with-polynomials/)

