# Universal Workflow Gate — Stage A implementation

**Status:** Executable local prototype for review; not an approved policy engine or production release authority.  
**Tracking issue:** https://github.com/KyleAlexanderSteen/GAIA-Documentation/issues/339  
**Lifecycle rollout:** https://github.com/KyleAlexanderSteen/GAIA-Documentation/issues/161

## What is implemented

- Local JSON manifest validation for the currently enumerated nine control blocks.
- Version rejection, stable rule IDs, sorted findings/control results, and a pinned caller-supplied evaluation time.
- SHA-256 hashes of exact manifest bytes, schema bytes, and registry bytes, plus validator version.
- Separate structural, evidence, policy, and release-authorization layers.
- Synthetic fixtures and negative tests for malformed JSON, unsupported versions, missing acceptance criteria, self-supersession, missing N/A justification, and deliberate invariant mutation.
- CI runs the deterministic test suite; the validator itself makes no network calls.
- Optional report writing is restricted to the configured output directory (or current working directory if unset), and refuses to overwrite an existing file.

## Explicit limitations and fail-closed behavior

- The source specification requires ten control blocks but lists nine in its example. The registry records only those nine and adds blocking finding GATE-01; it does not invent a tenth control.
- Identity strings and evidence declarations are not cryptographic identity or independent verification. GATE-06 is blocking.
- No owner decisions are guessed for applicability, exemptions, waivers, TTLs, trusted identity, or supported-version migrations.
- No trusted approval receipt exists. The report always sets releaseAuthorization to not-authorized and never emits release_authorized.
- The current CLI accepts JSON only. YAML parsing, schema migration, full JSON Schema engine validation, external reference resolution, evidence TTL evaluation, and production release authorization are not implemented.
- Exit code 0 means the input could be evaluated without structural errors; it does not mean passed, approved, safe, or releasable.
- The report hash binds exact manifest bytes. Semantically equivalent JSON with different whitespace has a different hash by design.

## Run locally

Node.js 22 or newer is required.

```sh
npm test
node src/workflow-gate-cli.js test/fixtures/workflow-valid-but-unverified.json --evaluation-time 2026-10-17T00:00:00.000Z
```

For a report file, set an output root and select a path beneath it:

```sh
mkdir -p .local-gate-output
GAIA_GATE_OUTPUT_DIR="$PWD/.local-gate-output" node src/workflow-gate-cli.js test/fixtures/workflow-valid-but-unverified.json --evaluation-time 2026-10-17T00:00:00.000Z --output "$PWD/.local-gate-output/report.json"
```

The validator does not fetch URLs or execute workflow code. A URI in a manifest is treated as a declared string, not dereferenced.

## Next required owner/review decisions

1. Resolve the canonical control inventory and schema consistency (GATE-01).
2. Approve supported versions and migration behavior.
3. Define trusted identity and independent verifier sources (GATE-06).
4. Define evidence digest semantics, TTLs, and freshness policy.
5. Define waiver, exemption, and non-waivable-control policy.
6. Bind a trusted approval receipt to the exact evaluated manifest/evidence before any future release authorization.

This Stage A implementation does not close issue 339 or 161. It supplies an executable, testable baseline for review and further falsification.
