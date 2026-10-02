# 이 저장소에서 글을 올리는 방법 (Claude Code용)

이 저장소는 Organization 멤버가 자연어로 Claude Code에 요청하면, 대신
git 작업을 수행해 글을 올리는 것을 전제로 합니다. 아래 순서를 그대로
따르세요.

## 새 글 작성 절차

1. 먼저 `main`을 최신 상태로 갱신: `git checkout main && git pull`
2. `main`에서 브랜치 생성: `post/YYYY-MM-DD-제목` (오늘 날짜, 제목은
   짧은 영문/숫자/하이픈으로 슬러그화)
3. `_posts/YYYY-MM-DD-title.md` 파일을 만들고 아래 front matter 형식을
   정확히 지킬 것:

   ```yaml
   ---
   title: "글 제목"
   date: YYYY-MM-DD
   author: "요청한 사람의 GitHub 아이디"
   categories: [분류1]
   ---
   ```

   `author`에 들어갈 GitHub 아이디를 모르는 경우, 요청한 사람 본인의
   글이라면 `gh api user --jq .login`으로 현재 인증된 계정의 아이디를
   조회할 수 있습니다. 다른 사람을 대신해 올리는 경우에는 반드시
   본인에게 GitHub 아이디를 직접 확인하세요.

   스터디 회차를 정리하는 글이라면 `session`(회차 번호) 필드를 추가로
   넣으세요. `session`이 있는 글은 `/sessions/` 페이지에 회차별로 자동
   정리됩니다:

   ```yaml
   ---
   title: "글 제목"
   date: YYYY-MM-DD
   author: "요청한 사람의 GitHub 아이디"
   categories: [분류1]
   session: 1
   ---
   ```

   미니 프로젝트 글은 `session` 대신 `categories: [미니 프로젝트]`로
   넣으세요. `/sessions/` 페이지 맨 아래 "미니 프로젝트" 영역에 자동으로
   모입니다.

   발표자가 만든 심화자료 HTML 파일(예:
   `블록체인_인프라_스터디자료.html`)이 있다면, 원본 그대로
   `assets/materials/YYYY-MM-DD-slug.html`에 복사해서 함께 커밋하고,
   포스트 본문에는 핵심 요약 몇 줄과 함께 아래처럼 링크를 넣으세요
   (파일 내용을 변환하거나 다시 쓰지 말고 그대로 복사할 것):

   ```markdown
   [전체 자료 보기]({{ "/assets/materials/YYYY-MM-DD-slug.html" | relative_url }})
   ```
4. 커밋 메시지는 `Add post: <제목>` 형식으로 작성
5. `git push -u origin <브랜치명>`으로 브랜치를 원격에 먼저 push할 것
   (비대화형 실행 환경에서는 `gh pr create`가 push 여부를 물어보는
   프롬프트에 응답할 수 없으므로, 반드시 push를 먼저 해야 함)
6. `gh pr create --title "..." --body "..."`로 PR을 생성. PR 본문은
   `.github/PULL_REQUEST_TEMPLATE.md`의 체크리스트를 채워서 작성
7. **PR을 올린 뒤에는 절대 스스로 병합(merge)하지 말 것.** 반드시
   사람이 리뷰하고 승인한 뒤에, 리뷰어 또는 작성자가 Merge 버튼으로
   직접 병합해야 배포가 시작됩니다. 승인만으로는 병합·배포가 되지
   않습니다.

## 로컬 미리보기

로컬에 Ruby/Jekyll이 없어도 괜찮습니다. 미리보기는 필수가 아니며,
PR을 올리면 `build-check` GitHub Actions가 자동으로 빌드 오류를
잡아줍니다.

## 하지 말아야 할 것

- `main` 브랜치에 직접 커밋/푸시하지 않기
- 스스로 PR을 병합하지 않기
- front matter의 네 개 필드(`title`, `date`, `author`, `categories`)를
  빠뜨리지 않기
- 심화자료 HTML 파일의 내용을 변환·재작성하지 않고 원본 그대로
  `assets/materials/`에 복사하기
