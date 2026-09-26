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

forbidden_snippets = ["deploy-pages", "gh-pages", "actions/deploy-pages"]
found_deploy = [s for s in forbidden_snippets if s in workflow]

if found_deploy:
    print(f"FAIL: workflow must not contain a deploy step: {found_deploy}")
    sys.exit(1)

print("PASS: build-check workflow has required sections")
