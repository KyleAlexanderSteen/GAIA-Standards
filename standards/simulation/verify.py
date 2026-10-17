#!/usr/bin/env python3
"""Independent verification pass for the simulation standard.

Re-loads the scenarios, confirms required fields and unique IDs, and re-runs the evaluator.
Second check after integration.
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SCENARIOS = ROOT / "reference_scenarios.json"
RUNNER = ROOT / "run_scenarios.py"

def main() -> int:
    if not SCENARIOS.is_file() or not RUNNER.is_file():
        print("missing scenarios or runner", file=sys.stderr)
        return 1
    data = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        print("scenarios must be a non-empty list", file=sys.stderr)
        return 1
    ids = [s.get("id") for s in data]
    if any(not i for i in ids) or len(ids) != len(set(ids)):
        print("scenario ids missing or not unique", file=sys.stderr)
        return 1
    for s in data:
        for key in ("seed", "events", "invariants"):
            if key not in s:
                print(f"{s.get('id')} missing {key}", file=sys.stderr)
                return 1
    result = subprocess.run([sys.executable, str(RUNNER)])
    if result.returncode != 0:
        print("runner failed verification", file=sys.stderr)
        return 1
    print("simulation verification: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
