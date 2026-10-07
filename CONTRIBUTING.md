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

   스터디 회차 정리 글이라면 `session`(회차 번호) 필드도 추가하세요.
   `session`이 있는 글은 [회차별 아카이브](/sessions/) 페이지에 자동으로
   모입니다.

   발표 때 만든 심화자료 HTML이 있다면, 원본 그대로
   `assets/materials/YYYY-MM-DD-slug.html`에 올려두고 본문에 요약과
   함께 링크를 남기세요:

   ```markdown
   [전체 자료 보기]({{ "/assets/materials/YYYY-MM-DD-slug.html" | relative_url }})
   ```

3. PR을 올리면 `build-check`가 자동으로 빌드를 확인합니다
4. `build-check`가 통과하면 작성자가 직접 Merge 버튼으로 병합합니다.
   리뷰 승인은 필요하지 않습니다 — 병합이 완료된 시점에 Pages 배포가
   시작됩니다

## 리뷰

- 리뷰 승인 없이도 작성자가 직접 병합할 수 있습니다
- 단, `main`에 직접 푸시하는 것은 금지되어 있으며 이력 관리를 위해
  반드시 PR을 거쳐 병합해야 합니다
- 리뷰는 필수가 아니지만, Organization 멤버 누구나 코멘트로 의견을
  남길 수 있습니다
