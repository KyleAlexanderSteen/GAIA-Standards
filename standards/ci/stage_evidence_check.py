#!/usr/bin/env python3
"""Minimal reference checker for the stage-evidence standard.

Reads a PR body from stdin or --body and exits non-zero if the Stage reached
section is missing or if checked stages lack basic evidence markers.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

STAGES = [
    "SPECIFICATION",
    "IMPLEMENTATION",
    "TEST",
    "INTEGRATION",
    "VERIFICATION",
    "OPERATIONAL",
]

def parse(body: str) -> dict:
    stage_section = re.search(r"## Stage reached(.*?)(?:\n## |\Z)", body, re.DOTALL | re.IGNORECASE)
    if not stage_section:
        return {"error": "missing ## Stage reached section"}
    text = stage_section.group(1)
    checked = []
    for stage in STAGES:
        if re.search(rf"- \[x\] {stage}\b", text, re.IGNORECASE):
            checked.append(stage)
    return {"checked": checked, "evidence": body}

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--body", type=Path)
    args = p.parse_args()
    body = args.body.read_text(encoding="utf-8") if args.body else sys.stdin.read()
    result = parse(body)
    if "error" in result:
        print(result["error"], file=sys.stderr)
        return 1
    if not result["checked"]:
        print("no stages checked", file=sys.stderr)
        return 1
    if "IMPLEMENTATION" in result["checked"] and not re.search(r"IMPLEMENTATION:\s*\S", body):
        print("IMPLEMENTATION checked but no evidence line", file=sys.stderr)
        return 1
    if "TEST" in result["checked"] and not re.search(r"TEST:\s*\S", body):
        print("TEST checked but no evidence line", file=sys.stderr)
        return 1
    print(f"stage-evidence check: PASS ({', '.join(result['checked'])})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
