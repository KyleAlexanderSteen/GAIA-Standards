#!/usr/bin/env python3
"""Independent verification pass for the template standard.

Re-reads the templates and confirms the contract is present.
This is a second check, separate from the unit tests and the integration validator.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).parent
REQUIRED_FILES = ["issue-template.md", "pull_request_template.md", "validate_templates.py", "test_templates.py"]
REQUIRED_STRINGS = {
    "issue-template.md": ["GAP-ID", "Acceptance criteria", "Stages", "Evidence plan"],
    "pull_request_template.md": ["Stage reached", "Evidence", "GAP-ID", "SPECIFICATION", "TEST"],
}

def main() -> int:
    errors = []
    for name in REQUIRED_FILES:
        if not (ROOT / name).is_file():
            errors.append(f"missing file: {name}")
    for name, needles in REQUIRED_STRINGS.items():
        path = ROOT / name
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for n in needles:
                if n not in text:
                    errors.append(f"{name} missing required string: {n}")
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("template verification: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
