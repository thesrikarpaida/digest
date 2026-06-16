---
layout: page
icon: fas fa-pen-nib
order: 3
title: WRITEUPS
---

<p class="digest-intro">My own write-ups — TryHackMe rooms, notes, and the occasional longer piece. Separate from the auto-curated digest.</p>

{% assign posts = site.posts | sort: "date" | reverse -%}
<div class="digest">
{%- for post in posts -%}
<a class="digest-item" href="{{ post.url | relative_url }}"><span class="digest-item__row"><span class="digest-item__title">{{ post.title | escape }}</span></span><span class="digest-item__tags">{{ post.date | date: "%b %-d, %Y" }}{% if post.tags.size > 0 %} · {% for t in post.tags %}{{ t | escape }}{% unless forloop.last %} · {% endunless %}{% endfor %}{% endif %}</span></a>
{%- endfor -%}
</div>
