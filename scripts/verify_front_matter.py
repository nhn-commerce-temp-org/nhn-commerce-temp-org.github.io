import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ["title", "date", "author", "categories"]

def extract_front_matter(text: str) -> str:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
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
