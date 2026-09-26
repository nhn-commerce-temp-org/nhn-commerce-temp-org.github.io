# Organization 기반 다중 저자 GitHub 블로그 설계

- 날짜: 2026-09-26
- 가제 Organization/리포지토리 이름: `my-blog-org` (추후 실제 이름으로 변경 예정)

## 배경 / 목표

개인 GitHub 계정으로 이미 Jekyll 기반 블로그를 운영 중이며, 별도로 GitHub
Organization 소속 여러 명이 동시에 글을 올리고 관리할 수 있는 팀 블로그를
새로 만든다. 개인 블로그와는 별개의 주제로 운영되며, 스택은 기존 개인
블로그와 동일하게 Jekyll + GitHub Pages를 사용한다.

## 1. 저장소 & 배포 구조

- Organization 생성 (가제: `my-blog-org`), 소속 리포지토리 `my-blog-org.github.io`
  생성
- GitHub Pages는 **"Deploy from a branch"** 방식 사용 (`main` 브랜치 소스)
  - GitHub Pages 내장 Jekyll 빌더가 push 시 자동 빌드/배포
  - `github-pages` gem이 허용하는 플러그인 범위 내에서 동작 (커스텀
    플러그인/특수 분석 도구가 필요해지면 그때 GitHub Actions 커스텀 빌드로
    전환)
- 커스텀 도메인 없음, 기본 `https://my-blog-org.github.io` 사용

### Organization/리포지토리 이름 변경

- Organization 이름은 Settings → General → Organization name 에서 언제든
  변경 가능
- `<org>.github.io` 리포지토리는 Organization 이름과 정확히 일치해야
  User/Org 페이지로 인식되므로, org 이름 변경 시 리포지토리도 함께
  rename 필요 (히스토리/이슈/PR은 유지됨)
- 이전 URL은 새 이름으로 자동 리다이렉트되지만 영구 보장은 아니므로,
  외부에 이미 공유된 링크가 있다면 깨질 수 있음
- 로컬 git remote URL도 이름 변경 후 갱신 필요

## 2. 권한 & 브랜치 보호 구조

- Organization 멤버는 모두 리포지토리에 대해 Write 권한 보유 (base
  permission 또는 팀 단위 Write 부여)
- `main` 브랜치 보호 규칙:
  - 직접 push 금지, PR을 통해서만 병합
  - 최소 1인 이상 리뷰 승인 필수
  - 리뷰어 강제 지정(CODEOWNERS)은 생략 — "누구나 작성 가능" 원칙에 맞춰
    가볍게 운영, PR 템플릿에 리뷰 요청 안내만 포함

## 3. 콘텐츠 작성 워크플로우

- 브랜치 네이밍: `post/YYYY-MM-DD-제목`
- 글 파일: `_posts/YYYY-MM-DD-title.md`
- Front matter에 작성자 정보 포함:

  ```yaml
  ---
  title: "제목"
  date: 2026-09-26
  author: "github-아이디"
  categories: [분류]
  ---
  ```

- 레이아웃(`_layouts/post.html`)에서 `page.author`를 읽어 글마다 작성자
  표시 (아바타는 `https://github.com/{author}.png`로 간단히 구성)
- 작성 흐름: 브랜치 생성 → 로컬 `bundle exec jekyll serve`로 미리보기 →
  PR 생성 → 리뷰 승인 → `main` 머지 → GitHub Pages 자동 빌드/배포
- PR 템플릿(`.github/PULL_REQUEST_TEMPLATE.md`)에 체크리스트 제공:
  오탈자 확인, 카테고리 지정, 로컬 미리보기 확인 여부 등

## 4. 검증 / CI

- GitHub Pages 기본 빌더는 merge 후 `main`에서만 빌드되므로, PR 단계
  오류를 미리 잡기 위한 검증 전용 GitHub Actions 워크플로우 하나를 추가:
  - PR open 시 `bundle exec jekyll build` 실행, 빌드 에러(front matter
    오타, 문법 오류 등) 체크
  - 배포 자체는 여전히 Pages의 "Deploy from a branch" 방식이 담당 (역할
    분리: Actions는 검증만, 배포는 Pages가 담당)
- `html-proofer` 등 링크/이미지 체크 도구는 초기엔 생략 (YAGNI), 필요시
  추후 추가

## 5. 테마 / 디자인

- 미정. 개인 블로그 테마를 그대로 가져올 필요는 없다고 판단 (완전히
  다른 주제로 운영될 예정이므로). 우선 Jekyll 기본 테마(minima)로
  시작하고, 블로그 주제가 정해지면 그에 맞는 방향으로 별도 결정
- 필요한 부분(레이아웃 구조 등)은 기존 개인 블로그에서 참고 가능

## 6. 초기 셋업 순서

1. GitHub Organization 생성 (가제 이름, 추후 rename)
2. `<org>.github.io` 리포지토리 생성, Jekyll 초기 스캐폴드
   (`bundle exec jekyll new .`)
3. Organization 멤버 초대, base permission "Write" 설정
4. `main` 브랜치 보호 규칙 설정 (PR 필수 + 1 approval)
5. PR 템플릿 + 글쓰기 가이드(`CONTRIBUTING.md`) 작성 (front matter 규칙
   포함)
6. PR 빌드 검증용 GitHub Actions 워크플로우 추가
7. Settings → Pages에서 "Deploy from a branch: main" 설정
8. 테마는 기본(minima)으로 시작, 이후 주제 확정되면 별도 결정

## 스코프 밖 (초기 단계에서 제외)

- 커스텀 도메인 연결
- CODEOWNERS를 통한 강제 리뷰어 지정
- html-proofer 등 추가 링크/이미지 검증 도구
- GitHub Actions 커스텀 빌드 (Pages 내장 빌더로 충분한 동안 불필요)
