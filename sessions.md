---
layout: page
title: 회차별 아카이브
permalink: /sessions/
---

`session` 값이 있는 스터디 포스트를 회차별로 묶어서 보여줍니다.

{% assign sessioned_posts = site.posts | where_exp: "post", "post.session" %}
{% assign sessions = sessioned_posts | group_by: "session" | sort: "name" %}
{% for group in sessions %}
### 회차 {{ group.name }}

<ul>
{% for post in group.items %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    — {{ post.author }}{% if post.categories.size > 0 %} ({{ post.categories | join: ", " }}){% endif %}
  </li>
{% endfor %}
</ul>
{% endfor %}

{% if sessions.size == 0 %}
아직 `session` 필드가 있는 포스트가 없습니다.
{% endif %}
