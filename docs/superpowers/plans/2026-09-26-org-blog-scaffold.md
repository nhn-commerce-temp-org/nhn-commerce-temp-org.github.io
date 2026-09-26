# Org Blog Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold a Jekyll-based, multi-author GitHub Organization blog repo (`my-blog-org.github.io` placeholder) that non-developer authors can operate entirely through Claude Code, with PR-based review and GitHub Actions build validation.

**Architecture:** Plain-file Jekyll site (no build tooling required to author it) using GitHub Pages' built-in Jekyll builder for deploy, a GitHub Actions workflow for PR-time build validation, and a `CLAUDE.md` that encodes the posting workflow for AI agents. All files are authorable and reviewable without running Ruby locally.

**Tech Stack:** Jekyll (via GitHub Pages built-in builder, `github-pages` gem), GitHub Actions, Markdown/YAML front matter.

**Spec:** `docs/superpowers/specs/2026-09-26-org-blog-design.md`

## Global Constraints

- Deploy method: GitHub Pages "Deploy from a branch" (`main`), not a custom Actions deploy — per spec section 1.
- No custom domain; site serves at `https://<org>.github.io` — per spec section 1.
- `main` is protected: PR + 1 approval required, no direct pushes — per spec section 2.
- Reviewer approval is the primary safety net (authors mostly don't read diffs themselves) — per spec section 2.
- Local Jekyll preview is optional, never required — per spec section 3.
- Front matter schema is exactly `title`, `date`, `author`, `categories` — per spec section 3.
- Post files live at `_posts/YYYY-MM-DD-title.md`; branches are named `post/YYYY-MM-DD-제목` — per spec section 3.
- This local environment has no Ruby/Jekyll/`gh` CLI installed — all verification in this plan is done with plain Python/text checks, not `jekyll build`. Real build verification happens via the GitHub Actions workflow after the repo is pushed to the actual GitHub org (out of scope for this plan's automated steps) — per user decision during brainstorming.

---

### Task 1: Jekyll site skeleton

**Files:**
- Create: `_config.yml`
- Create: `Gemfile`
- Create: `.gitignore`
- Create: `index.md`
- Test: `scripts/verify_config.py`

**Interfaces:**
- Produces: `_config.yml` with `title`, `theme: minima`, `permalink: /:year/:month/:day/:title/` — later tasks (layout, posts) rely on `theme: minima` being present so the default layout can be overridden.

- [ ] **Step 1: Create `_config.yml`**

```yaml
title: My Blog Org
description: "Organization 소속 여러 명이 함께 쓰는 블로그"
theme: minima
permalink: /:year/:month/:day/:title/
markdown: kramdown
```

- [ ] **Step 2: Create `Gemfile`**

```ruby
source "https://rubygems.org"

gem "github-pages", group: :jekyll_plugins
```

- [ ] **Step 3: Create `.gitignore`**

```
_site/
.bundle/
vendor/
.jekyll-cache/
.jekyll-metadata
```

- [ ] **Step 4: Create `index.md`**

```markdown
---
layout: home
---
```

- [ ] **Step 5: Write a verification script**

Create `scripts/verify_config.py`:

```python
import re
import sys

with open("_config.yml", encoding="utf-8") as f:
    config = f.read()

required = ["title:", "theme: minima", "permalink:"]
missing = [key for key in required if key not in config]

if missing:
    print(f"FAIL: _config.yml missing keys: {missing}")
    sys.exit(1)

print("PASS: _config.yml has required keys")
```

- [ ] **Step 6: Run the verification script**

Run: `python scripts/verify_config.py`
Expected: `PASS: _config.yml has required keys`

- [ ] **Step 7: Commit**

```bash
git add _config.yml Gemfile .gitignore index.md scripts/verify_config.py
git commit -m "Add Jekyll site skeleton"
```

---

### Task 2: Author-aware post layout + example post

**Files:**
- Create: `_layouts/post.html`
- Create: `_posts/2026-09-26-welcome-to-the-blog.md`
- Test: `scripts/verify_front_matter.py`

**Interfaces:**
- Consumes: `theme: minima` from Task 1 (`_layouts/post.html` overrides minima's default post layout of the same name).
- Produces: front matter schema (`title`, `date`, `author`, `categories`) that Task 5 (`CLAUDE.md`) and Task 6 (PR template) both document and rely on authors following.

- [ ] **Step 1: Create the post layout override**

Create `_layouts/post.html`:

```html
---
layout: default
---
<article class="post">
  <header class="post-header">
    <h1 class="post-title">{{ page.title }}</h1>
    <p class="post-meta">
      <img class="author-avatar" src="https://github.com/{{ page.author }}.png" width="24" height="24" alt="{{ page.author }}">
      <span>{{ page.author }}</span>
      · <time datetime="{{ page.date | date_to_xmlschema }}">{{ page.date | date: "%Y-%m-%d" }}</time>
      {% if page.categories.size > 0 %}
      · {{ page.categories | join: ", " }}
      {% endif %}
    </p>
  </header>
  <div class="post-content">
    {{ content }}
  </div>
</article>
```

- [ ] **Step 2: Create an example post**

Create `_posts/2026-09-26-welcome-to-the-blog.md`:

```markdown
---
title: "블로그를 시작합니다"
date: 2026-09-26
author: "octocat"
categories: [공지]
---

이 블로그는 Organization 멤버 여러 명이 함께 운영합니다. 새 글을 쓰려면
`CLAUDE.md`에 정리된 워크플로우를 참고하세요.
```

- [ ] **Step 3: Write a front matter verification script**

Create `scripts/verify_front_matter.py`:

```python
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ["title", "date", "author", "categories"]

def extract_front_matter(text: str) -> str:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return None
    return match.group(1)

failures = []
for path in Path("_posts").glob("*.md"):
    text = path.read_text(encoding="utf-8")
    front_matter = extract_front_matter(text)
    if front_matter is None:
        failures.append(f"{path}: no front matter block found")
        continue
    for field in REQUIRED_FIELDS:
        if not re.search(rf"^{field}:", front_matter, re.MULTILINE):
            failures.append(f"{path}: missing '{field}:' field")

if failures:
    print("FAIL:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)

print("PASS: all posts have required front matter fields")
```

- [ ] **Step 4: Run the verification script**

Run: `python scripts/verify_front_matter.py`
Expected: `PASS: all posts have required front matter fields`

- [ ] **Step 5: Commit**

```bash
git add _layouts/post.html "_posts/2026-09-26-welcome-to-the-blog.md" scripts/verify_front_matter.py
git commit -m "Add author-aware post layout and example post"
```

---

### Task 3: PR template

**Files:**
- Create: `.github/PULL_REQUEST_TEMPLATE.md`
- Test: manual read-through (no script — this is a text template, checked in Step 2)

**Interfaces:**
- Consumes: front matter schema from Task 2 (checklist item names the same four fields).

- [ ] **Step 1: Create the PR template**

Create `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## 이 PR은 무엇을 올리나요?

<!-- 글 제목과 간단한 요약을 적어주세요 -->

## 체크리스트

- [ ] `_posts/YYYY-MM-DD-title.md` 형식으로 파일을 만들었어요
- [ ] front matter에 `title`, `date`, `author`, `categories`를 모두 채웠어요
- [ ] CI 빌드 체크(`build-check`)가 통과했어요
- [ ] (선택) 로컬에서 미리보기를 확인했어요

## 리뷰어에게

이 저장소는 Organization 멤버 누구나 리뷰/승인할 수 있습니다. 내용을 한 번
훑어보고 이상 없으면 승인해주세요.
```

- [ ] **Step 2: Verify the template renders as expected**

Run: `python -c "print(open('.github/PULL_REQUEST_TEMPLATE.md', encoding='utf-8').read())"`
Expected: prints the template with the four front matter fields named exactly as in `_posts/2026-09-26-welcome-to-the-blog.md` (title, date, author, categories).

- [ ] **Step 3: Commit**

```bash
git add .github/PULL_REQUEST_TEMPLATE.md
git commit -m "Add PR template"
```

---

### Task 4: GitHub Actions PR build-check workflow

**Files:**
- Create: `.github/workflows/build-check.yml`
- Test: `scripts/verify_workflow.py`

**Interfaces:**
- Produces: a CI job named `build-check` that Task 3's PR template references and that spec section 5 requires (validation only, no deploy).

- [ ] **Step 1: Create the workflow**

Create `.github/workflows/build-check.yml`:

```yaml
name: build-check

on:
  pull_request:
    branches: [main]

jobs:
  build-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
          bundler-cache: true
      - name: Build with Jekyll
        run: bundle exec jekyll build
```

- [ ] **Step 2: Write a workflow verification script**

Create `scripts/verify_workflow.py`:

```python
import sys

with open(".github/workflows/build-check.yml", encoding="utf-8") as f:
    workflow = f.read()

required_snippets = [
    "name: build-check",
    "on:",
    "pull_request:",
    "jobs:",
    "bundle exec jekyll build",
]
missing = [s for s in required_snippets if s not in workflow]

if missing:
    print(f"FAIL: workflow missing: {missing}")
    sys.exit(1)

print("PASS: build-check workflow has required sections")
```

- [ ] **Step 3: Run the verification script**

Run: `python scripts/verify_workflow.py`
Expected: `PASS: build-check workflow has required sections`

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/build-check.yml scripts/verify_workflow.py
git commit -m "Add PR build-check GitHub Actions workflow"
```

---

### Task 5: CLAUDE.md / AGENTS.md for AI-authoring workflow

**Files:**
- Create: `CLAUDE.md`
- Create: `AGENTS.md`
- Test: manual read-through (Step 2)

**Interfaces:**
- Consumes: branch naming (`post/YYYY-MM-DD-제목`) and front matter schema from Task 2; PR template fields from Task 3.

- [ ] **Step 1: Create `CLAUDE.md`**

Create `CLAUDE.md`:

```markdown
# 이 저장소에서 글을 올리는 방법 (Claude Code용)

이 저장소는 Organization 멤버가 자연어로 Claude Code에 요청하면, 대신
git 작업을 수행해 글을 올리는 것을 전제로 합니다. 아래 순서를 그대로
따르세요.

## 새 글 작성 절차

1. `main`에서 브랜치 생성: `post/YYYY-MM-DD-제목` (오늘 날짜, 제목은
   짧은 영문/숫자/하이픈으로 슬러그화)
2. `_posts/YYYY-MM-DD-title.md` 파일을 만들고 아래 front matter 형식을
   정확히 지킬 것:

   ```yaml
   ---
   title: "글 제목"
   date: YYYY-MM-DD
   author: "요청한 사람의 GitHub 아이디"
   categories: [분류1]
   ---
   ```

3. 커밋 메시지는 `Add post: <제목>` 형식으로 작성
4. `gh pr create --title "..." --body "..."`로 PR을 생성. PR 본문은
   `.github/PULL_REQUEST_TEMPLATE.md`의 체크리스트를 채워서 작성
5. **PR을 올린 뒤에는 절대 스스로 병합(merge)하지 말 것.** 반드시
   사람이 리뷰하고 승인한 뒤에 병합되어야 합니다.

## 로컬 미리보기

로컬에 Ruby/Jekyll이 없어도 괜찮습니다. 미리보기는 필수가 아니며,
PR을 올리면 `build-check` GitHub Actions가 자동으로 빌드 오류를
잡아줍니다.

## 하지 말아야 할 것

- `main` 브랜치에 직접 커밋/푸시하지 않기
- 스스로 PR을 병합하지 않기
- front matter의 네 개 필드(`title`, `date`, `author`, `categories`)를
  빠뜨리지 않기
```

- [ ] **Step 2: Create `AGENTS.md` as a pointer**

Create `AGENTS.md`:

```markdown
# Agents

이 저장소에서 AI 에이전트가 따라야 할 작업 절차는 `CLAUDE.md`에
정리되어 있습니다. 그 문서의 내용을 그대로 따르세요.
```

- [ ] **Step 3: Read through both files for consistency**

Run: `python -c "a=open('CLAUDE.md',encoding='utf-8').read(); b=open('AGENTS.md',encoding='utf-8').read(); print('CLAUDE.md len:', len(a)); print('AGENTS.md len:', len(b))"`
Expected: both files print a non-zero length (confirms both were written and are readable).

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md AGENTS.md
git commit -m "Add CLAUDE.md/AGENTS.md AI-authoring workflow"
```

---

### Task 6: CONTRIBUTING.md (human-facing guide)

**Files:**
- Create: `CONTRIBUTING.md`
- Test: manual read-through (Step 2)

**Interfaces:**
- Consumes: same workflow facts as Task 5, written for a human reader instead of an agent.

- [ ] **Step 1: Create `CONTRIBUTING.md`**

Create `CONTRIBUTING.md`:

```markdown
# 글쓰기 가이드

이 블로그는 Organization 멤버 누구나 글을 올릴 수 있습니다. Claude Code를
쓰고 있다면 그냥 "이런 내용으로 글 써서 올려줘"라고 요청하세요 —
`CLAUDE.md`에 정리된 절차를 따라 브랜치 생성부터 PR까지 대신
처리해줍니다.

## 직접 작성하는 경우

1. `main`에서 `post/YYYY-MM-DD-제목` 브랜치를 만드세요
2. `_posts/YYYY-MM-DD-title.md` 파일을 만들고 아래 형식을 채우세요:

   ```yaml
   ---
   title: "글 제목"
   date: YYYY-MM-DD
   author: "본인 GitHub 아이디"
   categories: [분류]
   ---
   ```

3. PR을 올리면 `build-check`가 자동으로 빌드를 확인합니다
4. 다른 멤버의 리뷰 승인을 받으면 자동으로 배포됩니다

## 리뷰

- 리뷰어는 Organization 멤버 누구나 가능합니다 (본인 PR 제외)
- 최소 1명의 승인이 있어야 병합할 수 있습니다
```

- [ ] **Step 2: Confirm the front matter example matches Task 2's schema**

Run: `python -c "c=open('CONTRIBUTING.md',encoding='utf-8').read(); fields=['title:','date:','author:','categories:']; print(all(f in c for f in fields))"`
Expected: `True`

- [ ] **Step 3: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "Add CONTRIBUTING.md"
```

---

### Task 7: README with manual GitHub setup steps

**Files:**
- Create: `README.md`
- Test: manual read-through (Step 2)

**Interfaces:**
- Consumes: org/repo naming and rename procedure from spec section 1; permission/branch-protection settings from spec section 2; Pages settings from spec section 1.

- [ ] **Step 1: Create `README.md`**

Create `README.md`:

```markdown
# my-blog-org.github.io

Organization 소속 여러 명이 함께 운영하는 Jekyll 블로그. 자세한 설계는
`docs/superpowers/specs/2026-09-26-org-blog-design.md` 참고.

## 처음 설정할 때 (GitHub 웹에서 수동으로 해야 하는 것들)

1. **Organization 생성**: github.com에서 새 Organization 생성 (가제
   이름을 실제 이름으로 바로 정했다면 그 이름 사용)
2. **리포지토리 이름**: Organization 이름과 정확히 같은
   `<org-name>.github.io`로 생성 (또는 이 리포를 그대로 옮기고 rename)
3. **멤버 초대 + 권한**: Settings → Member privileges (또는
   People 탭에서 팀 생성) → 모든 멤버에게 Write 권한 부여
4. **브랜치 보호**: Settings → Branches → `main`에 규칙 추가:
   - "Require a pull request before merging" 체크
   - "Require approvals" 체크, 최소 1
5. **Pages 설정**: Settings → Pages → Build and deployment → Source:
   "Deploy from a branch" → Branch: `main` / `/ (root)`
6. **Organization/리포 이름을 나중에 바꾸는 경우**: Organization
   Settings에서 이름 변경 → 리포지토리 이름도 반드시 새
   `<org-name>.github.io`로 함께 변경 → 로컬 git remote URL 갱신

## 글쓰기

`CONTRIBUTING.md` (사람용) 또는 `CLAUDE.md` (Claude Code용) 참고.
```

- [ ] **Step 2: Confirm all five manual setup steps are present**

Run: `python -c "r=open('README.md',encoding='utf-8').read(); steps=['Organization 생성','리포지토리 이름','멤버 초대','브랜치 보호','Pages 설정']; print(all(s in r for s in steps))"`
Expected: `True`

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "Add README with manual GitHub setup steps"
```

---

## After this plan

Once all tasks are committed locally:

1. Create the real GitHub Organization and `<org-name>.github.io` repo (README Step 1-2, done by the user in a browser).
2. Push this local repo to the new remote (`git remote add origin ...`, `git push -u origin main`).
3. Follow README steps 3-5 (member invite, branch protection, Pages settings) in the GitHub web UI.
4. Open a test PR to confirm the `build-check` Actions workflow actually runs and passes — this is the first real Jekyll build validation, since it couldn't be run locally in this environment.
