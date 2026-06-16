---
layout: page
icon: fas fa-star
order: 1
title: TOP PICKS
---

<p class="digest-intro">The highest-impact items — the "if you only read one thing today" list, pulled from across every section.</p>

{% assign items = site.digest | where: "must_know", true | sort: "date" | reverse -%}
<div class="digest">
{%- assign last = "" -%}
{%- for post in items -%}
{%- assign d = post.date | date: "%A, %B %-d, %Y" -%}
{%- if d != last -%}
{%- unless forloop.first %}</div>{% endunless -%}
<h2 class="digest-date">{{ d }}</h2><div class="digest-day">
{%- assign last = d -%}
{%- endif -%}
<a class="digest-item" href="{{ post.url | relative_url }}"><span class="digest-item__row">{% if post.severity %}<span class="sev sev--{{ post.severity }}">{{ post.severity | upcase }}</span>{% endif %}<span class="digest-item__title">{{ post.title | escape }}</span></span>{% if post.tags.size > 0 %}<span class="digest-item__tags">{% for t in post.tags %}{{ t | escape }}{% unless forloop.last %} · {% endunless %}{% endfor %}</span>{% endif %}</a>
{%- endfor -%}
{%- unless items == empty %}</div>{% endunless -%}
</div>

<script>
  (function () {
    var link = document.querySelector('#breadcrumb span:first-child a');
    if (link) { link.textContent = 'Digest'; link.setAttribute('href', '{{ "/" | relative_url }}'); }
  })();
</script>
