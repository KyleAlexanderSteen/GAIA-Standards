#!/usr/bin/env python3
"""Independent verification pass for the stage-evidence standard.

Confirms the checker, fixtures, and tests exist and that the valid fixture passes
while the invalid fixture fails. Second check after integration.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
REQUIRED = ["stage_evidence_check.py", "test_stage_evidence_check.py", "fixtures/valid_pr.md", "fixtures/invalid_pr.md"]

def main() -> int:
    errors = []
    for name in REQUIRED:
        if not (ROOT / name).is_file():
            errors.append(f"missing: {name}")
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    valid = subprocess.run([sys.executable, str(ROOT / "stage_evidence_check.py"), "--body", str(ROOT / "fixtures/valid_pr.md")])
    if valid.returncode != 0:
        print("valid fixture failed verification", file=sys.stderr)
        return 1
    invalid = subprocess.run([sys.executable, str(ROOT / "stage_evidence_check.py"), "--body", str(ROOT / "fixtures/invalid_pr.md")])
    if invalid.returncode == 0:
        print("invalid fixture incorrectly passed", file=sys.stderr)
        return 1
    print("stage-evidence verification: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
