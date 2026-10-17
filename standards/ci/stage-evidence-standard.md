# CI stage-evidence standard

**Purpose:** Make pull requests fail closed when required stage evidence is missing.

This standard defines the minimum check that repositories should run in CI. It is a reference; the implementation may live in a shared workflow or be copied per repository.

## Required stages

A PR body must contain a section headed `## Stage reached` with checkboxes in the form `- [x] NAME` or `- [ ] NAME` where NAME is one of:

- SPECIFICATION
- IMPLEMENTATION
- TEST
- INTEGRATION
- VERIFICATION
- OPERATIONAL

## Rules

1. At least SPECIFICATION must be checked for any PR that claims to address an issue.
2. If IMPLEMENTATION is checked, at least one file path or commit SHA must appear in the Evidence section.
3. If TEST is checked, a command and a PASS/FAIL result on the exact head SHA must be present.
4. Missing, skipped, or pending required checks are not PASS.
5. The check itself does not grant merge authority. Human review remains required.

## Reference behavior (from legacy GAIA-3.0)

The legacy `pr-lifecycle.yml` and `tools/agent-skills/pr_lifecycle_check.py` already enforce related rules. New repositories should adopt an equivalent check.

## Minimal reference script

See `stage_evidence_check.py` in this directory. It is a starting point only; it does not replace repository-specific lifecycle tools.
