#!/usr/bin/env python3
"""Integration: load reference scenarios and evaluate basic invariants.

This is a minimal deterministic runner for the simulation standard.
It does not claim full verification; it produces PASS/FAIL for the reference set.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SCENARIOS = ROOT / "reference_scenarios.json"

def evaluate(scenario: dict) -> tuple[str, list[str]]:
    errors = []
    events = scenario.get("events", [])
    refused = set()
    executed = set()
    failures = []
    recovered = False
    for ev in events:
        kind = ev.get("kind")
        name = ev.get("name", kind)
        if kind == "execute":
            if ev.get("authorized", True):
                executed.add(name)
            else:
                refused.add(name)
        elif kind == "refuse":
            refused.add(name)
        elif kind == "inject_failure":
            failures.append(name)
        elif kind == "recover":
            recovered = True
        else:
            errors.append(f"unknown kind: {kind}")
    for inv in scenario.get("invariants", []):
        if inv == "refused_action_never_executes":
            overlap = refused & executed
            if overlap:
                errors.append(f"refused actions executed: {sorted(overlap)}")
        elif inv == "failure_is_recorded":
            if failures is None:
                errors.append("failure state unavailable")
        elif inv == "recovery_is_explicit":
            if failures and not recovered:
                errors.append("failure without explicit recovery")
        else:
            errors.append(f"unknown invariant: {inv}")
    return ("PASS" if not errors else "FAIL", errors)

def main() -> int:
    scenarios = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    failed = 0
    for s in scenarios:
        outcome, errors = evaluate(s)
        print(f"[{outcome}] {s['id']}")
        for e in errors:
            print(f"  - {e}")
        if outcome != "PASS":
            failed += 1
    if failed:
        print(f"{failed} scenario(s) failed", file=sys.stderr)
        return 1
    print("simulation integration: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
