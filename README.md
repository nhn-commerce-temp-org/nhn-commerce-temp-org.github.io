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
