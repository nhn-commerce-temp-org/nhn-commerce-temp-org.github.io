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
