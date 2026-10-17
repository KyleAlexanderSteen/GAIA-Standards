#!/usr/bin/env python3
"""Integration: validate that issue and PR template files contain the required contract sections.

This is the runnable integration for the research-backed templates standard.
Exits non-zero if any required section is missing.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).parent

ISSUE_REQUIRED = [
    "GAP-ID",
    "Acceptance criteria",
    "Stages",
    "SPECIFICATION",
    "IMPLEMENTATION",
    "TEST",
    "Evidence plan",
]
PR_REQUIRED = [
    "Stage reached",
    "SPECIFICATION",
    "IMPLEMENTATION",
    "TEST",
    "Evidence",
    "GAP-ID",
]

def check(path: Path, required: list[str]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [s for s in required if s not in text]

def main() -> int:
    errors = []
    issue = ROOT / "issue-template.md"
    pr = ROOT / "pull_request_template.md"
    if not issue.is_file():
        errors.append("missing issue-template.md")
    else:
        missing = check(issue, ISSUE_REQUIRED)
        if missing:
            errors.append(f"issue-template.md missing: {missing}")
    if not pr.is_file():
        errors.append("missing pull_request_template.md")
    else:
        missing = check(pr, PR_REQUIRED)
        if missing:
            errors.append(f"pull_request_template.md missing: {missing}")
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("template integration: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
