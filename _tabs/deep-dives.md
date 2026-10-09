---
layout: page
icon: fas fa-magnifying-glass-chart
order: 2
title: DEEP DIVES
digest_paginate: deep-dives
---

<p class="digest-intro">Longer-form analysis — kill chains, malware breakdowns, and post-mortems on the bigger stories.</p>

<div class="digest digest--cards">
{%- for post in page.digest_items -%}
<a class="digest-card" href="{{ post.url | relative_url }}"><span class="digest-card__head">{% if post.severity %}<span class="sev sev--{{ post.severity }}">{{ post.severity | upcase }}</span>{% endif %}<span class="digest-card__date">{{ post.date | date: "%b %-d, %Y" }}</span></span><span class="digest-card__title">{{ post.title | escape }}</span><span class="digest-card__excerpt">{{ post.excerpt | strip_html | truncatewords: 32 }}</span></a>
{%- endfor -%}
</div>
{% include digest-pager.html %}

<script>
  (function () {
    var link = document.querySelector('#breadcrumb span:first-child a');
    if (link) { link.textContent = 'Digest'; link.setAttribute('href', '{{ "/" | relative_url }}'); }
  })();
</script>
