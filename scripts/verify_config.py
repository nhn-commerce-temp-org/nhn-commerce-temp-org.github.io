import sys

with open("_config.yml", encoding="utf-8") as f:
    config = f.read()

required = ["title:", "theme: minima", "permalink:"]
missing = [key for key in required if key not in config]

if missing:
    print(f"FAIL: _config.yml missing keys: {missing}")
    sys.exit(1)

print("PASS: _config.yml has required keys")
