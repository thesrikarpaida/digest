---
layout: page
icon: fas fa-star
order: 1
title: TOP PICKS
digest_paginate: must_know
---

<p class="digest-intro">The highest-impact items — the "if you only read one thing today" list, pulled from across every section.</p>

{% include digest-list.html items=page.digest_items %}
{% include digest-pager.html %}

<script>
  (function () {
    var link = document.querySelector('#breadcrumb span:first-child a');
    if (link) { link.textContent = 'Digest'; link.setAttribute('href', '{{ "/" | relative_url }}'); }
  })();
</script>
