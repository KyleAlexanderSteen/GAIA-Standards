# Simulation harness standard

**Purpose:** Provide a deterministic, offline way to record Pass / Fail / NeedVerify / OutOfScope against a gap or scenario before claiming verification.

This is a reference standard derived from the legacy GAIA-3.0 `tools/verification/simulation_gate.py`. Implementations may live in GAIA-Tools, GAIA-Core, or per-repository.

## Outcomes

- **PASS** — invariants held
- **FAIL** — invariant violated or runner error
- **NeedVerify** — result is provisional; human or additional evidence required
- **OutOfScope** — scenario does not apply to the current claim

A simulation outcome is not verification by itself.

## Rules

- Scenarios are data (JSON), not hidden logic.
- Results must be reproducible from the scenario file and seed.
- Gap-linked scenarios must cite a GAP-ID in the scenario metadata when used for research follow-up.
- Live external systems (planetary data, network agents, etc.) are out of scope for this harness.

## Reference

- `reference_scenarios.json` — starter scenarios including one gap-linked refuse example.
- Adopting repositories should copy or extend the runner pattern from the legacy tree.
