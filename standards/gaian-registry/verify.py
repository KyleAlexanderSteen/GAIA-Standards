#!/usr/bin/env python3
"""Independent verification for the GAIAN Registry schema and validator."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT.parent.parent / "schemas" / "gaian-registry-record.v1.json"
VALIDATOR = ROOT / "validate_record.py"
TESTS = ROOT / "test_validate_record.py"

def main() -> int:
    for p in (SCHEMA, VALIDATOR, TESTS):
        if not p.is_file():
            print(f"missing {p}", file=sys.stderr)
            return 1
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if schema.get("title") != "GAIAN Registry Record":
        print("unexpected schema title", file=sys.stderr)
        return 1
    if "grants_authority" not in schema.get("properties", {}):
        print("schema missing grants_authority", file=sys.stderr)
        return 1
    r = subprocess.run([sys.executable, "-m", "unittest", str(TESTS)])
    if r.returncode != 0:
        print("validator tests failed verification", file=sys.stderr)
        return 1
    print("gaian-registry verification: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
