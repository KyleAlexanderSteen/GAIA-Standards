# Research-backed issue and PR templates

Standard templates for turning a verified gap (from GAIA-Research) into an implementation issue and a PR that must show stage evidence.

These are the canonical forms. Repositories that accept issues and PRs should copy or adapt them into their `.github/` directory.

Source patterns: legacy GAIA-3.0 `.github/ISSUE_TEMPLATE/` and `PULL_REQUEST_TEMPLATE.md`, plus the research-simulate-verify playbook in GAIA-Research.

## Rules

- Every implementation issue must link a GAP-ID or an existing issue that already has acceptance criteria.
- A PR must list the stages it actually reaches and provide evidence for each.
- Stubs fail loudly. Description never grants authority.
- `Closes` is allowed only when OPERATIONAL evidence exists and acceptance criteria are met.
