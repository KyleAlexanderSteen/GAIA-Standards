# Proposed Workflow Provenance Event Contract

- **Status:** Proposed; owner review required before adoption.
- **Version:** 0.1.0
- **Tracking issue:** [GAIA-Documentation #320](https://github.com/KyleAlexanderSteen/GAIA-Documentation/issues/320)
- **Related requirements:** GAIA-Documentation issues #1, #5, #21, #172, and #183.
- **Implementation targets:** GAIA-Standards, GAIA-Security, GAIA-Monitoring, GAIA-Data-Pipeline.
- **Decision boundary:** This document defines a reviewable contract proposal. It does not select a ledger backend, signature algorithm, key-management system, identifier registry, transport, or deployment architecture.

## 1. Purpose and non-goals

The contract binds a business-process transition to the actor/workload, policy version, evidence and artifact references, outcome, and causal context that explain the transition. It distinguishes operational telemetry from authoritative audit evidence.

It does **not** claim that transport mTLS, trace IDs, workflow-engine history, or a software artifact attestation alone proves the complete business-process execution. It does not prescribe a production ledger or cryptographic signing protocol.

## 2. Event model

Every event MUST have the following fields:

| Field | Type / rule | Meaning |
|---|---|---|
| `schema_version` | non-empty version string | Exact event schema version used to validate this record |
| `event_id` | globally unique opaque identifier | Stable identity of this event; retries MUST preserve it |
| `workflow_id` | opaque identifier | Logical workflow instance |
| `transition_id` | opaque identifier | Logical transition or attempted transition |
| `sequence` | non-negative integer | Producer-assigned order within the workflow stream; not proof of causal order by itself |
| `occurred_at` | RFC 3339 timestamp with UTC offset | Time the transition is asserted to have occurred |
| `recorded_at` | RFC 3339 timestamp with UTC offset | Time this record was committed to the evidence system, when known |
| `actor` | structured identity object | Principal/workload responsible for initiating or executing the transition |
| `action` | non-empty namespaced string | Requested operation or transition name |
| `resource` | structured reference | Target resource, with sensitive identifiers minimized |
| `policy` | structured reference or explicit `null` | Policy identifier and immutable version/digest used for the decision |
| `evidence` | array of typed references | Evidence IDs, immutable digests, media types, and evidence state |
| `artifacts` | array of typed references | Artifact identity and digest when the transition depends on an artifact |
| `causation_ids` | array of event IDs | Events that directly caused this event |
| `correlation_id` | opaque identifier or explicit `null` | Join key for operational traces; never authoritative proof by itself |
| `outcome` | enum | `succeeded`, `failed`, `denied`, `approval_required`, `cancelled`, or `unknown` |
| `failure` | structured object or explicit `null` | Stable failure code and safe summary; no secrets or raw sensitive payloads |
| `integrity` | structured object or explicit `null` | Digest/checkpoint/signature metadata only when produced under an approved profile |

Unknown optional fields MAY be retained for forward compatibility, but consumers MUST reject unknown values for security-critical enumerations unless the schema version explicitly permits them. Required fields MUST NOT be silently defaulted.

### Identity object

The `actor` object MUST distinguish `kind` (for example `human`, `service`, `agent`, or `system`), a stable issuer-qualified subject reference, and the authentication/workload-identity evidence available to the producer. Display names alone are not identities. Missing or unverified identity evidence MUST be represented explicitly.

### Evidence and artifact references

Each reference MUST include a type, stable reference ID, and integrity digest when the referenced content is digestible. Include a digest algorithm identifier alongside the digest; the algorithm is not globally selected by this proposal. A reference to unavailable content MUST remain visibly unavailable and MUST NOT be treated as verified evidence. Sensitive payloads SHOULD be kept outside the event and linked through access-controlled references.

Evidence state MUST be one of:

- `verified`: integrity and required verification checks passed under a named verifier/profile.
- `reconstructed`: derived after the event from secondary sources; not equivalent to contemporaneous evidence.
- `unverified`: present but not verified.
- `unavailable`: referenced evidence could not be retrieved.
- `invalid`: a verification check failed.

A consumer MUST preserve this distinction through export, aggregation, migration, and reporting.

## 3. Time and causal semantics

- `occurred_at` is an assertion made by the producer, not a trusted clock proof.
- `recorded_at` MUST be assigned by the evidence sink or a trusted recorder when possible. If unavailable, it MUST be omitted or represented as unknown—not copied from `occurred_at`.
- UTC normalization is recommended for comparisons, while the original offset may be retained as source metadata.
- Wall-clock order MUST NOT replace causal links. `causation_ids` expresses direct causation; `sequence` is only a producer-local ordering hint.
- Clock skew, late arrival, duplicate delivery, gaps, and out-of-order events MUST be detectable and represented in verification results.
- Trace/correlation identifiers help join telemetry to audit evidence but do not make telemetry authoritative and MUST NOT be used as a substitute for event identity or integrity checks.

## 4. Serialization, digest, checkpoint, and signatures

The canonical serialization and cryptographic profile are **open decisions**. A candidate canonical JSON profile may be evaluated for deterministic byte representation, but no profile is adopted by this document.

Any eventual profile MUST define, test, and version:
1. UTF-8 encoding and canonical field ordering/number/string handling.
2. Digest algorithm identifiers and exact bytes covered by each digest.
3. How prior-event/checkpoint references are included without ambiguous self-reference.
4. Signature envelope, signed fields, algorithm agility rules, and verifier behavior.
5. Key creation, custody, rotation, expiry, revocation, compromise handling, and historical verification.
6. Checkpoint frequency, checkpoint authority, fork detection, and recovery after missing or corrupt records.
7. Domain separation and replay protections.

A TLS/mTLS session authenticates a connection under its configured trust model; it does not, by itself, sign this event, bind its evidence digests, or provide durable business-process provenance.

Until a profile is approved, `integrity` MUST be absent or explicitly marked as a proposal/test-only value. Implementations MUST NOT label an unsigned event as signed or verified.

## 5. Verification result contract

A verifier SHOULD return a structured result containing:

- `status`: `verified`, `partially_verified`, `reconstructed`, `unverified`, or `invalid`;
- `checks`: named checks, each with pass/fail/indeterminate and a safe reason code;
- `schema_version` and verifier/profile version;
- `checked_at` timestamp;
- `gaps`: missing events, evidence, checkpoints, or keys;
- `warnings`: clock, ordering, legacy, or trust limitations.

A failed or indeterminate check MUST NOT be collapsed into success. Legacy/reconstructed data MUST NOT be silently upgraded to verified provenance.

## 6. Operational audit and privacy

- Operational traces and metrics are query aids, not the authoritative audit record.
- The authoritative recorder MUST define acknowledgement semantics, append failure behavior, retention, deletion/legal-hold behavior, access control, and recovery.
- If a workflow requires durable evidence before a protected side effect, that side effect MUST NOT run until the required evidence write is durably acknowledged. The exact policy is a workflow risk decision and must be specified at the call site.
- Do not record credentials, bearer tokens, secret material, raw prompts, or unnecessary sensitive payloads. Prefer redacted summaries and access-controlled evidence references.
- Any deletion or redaction process MUST preserve a record of the integrity impact without retaining the sensitive content itself.
- A recorder outage, storage failure, or unavailable key service MUST be visible as a failure/indeterminate state; it MUST NOT be reported as successful audit persistence.

## 7. Threat and conformance matrix

| Threat / fault | Required conformance behavior |
|---|---|
| Event tampering | Digest/signature verification fails or reports indeterminate if no approved integrity profile exists |
| Truncation or missing event | Detect a sequence/checkpoint gap where the selected profile supports it; report incomplete chain |
| Reordering | Validate causal links and profile-specific ordering; do not infer causality from timestamps alone |
| Replay / duplicate delivery | Stable event ID and idempotent ingestion distinguish exact duplicate from conflicting reuse |
| Forked history | Compare checkpoint/parent references and report competing descendants where supported |
| Crash during append | Define atomicity/acknowledgement boundary; never claim durable success before it |
| Key rotation/expiry | Verify historical records under documented key-validity and revocation semantics; unresolved key status is not success |
| Compromised key | Mark affected trust interval and affected records according to the approved profile |
| Clock skew | Preserve source timestamps and report skew/order uncertainty |
| Missing evidence | Retain explicit unavailable/unverified state; never promote to verified |
| Telemetry loss | Audit verification remains independent of telemetry availability |
| Sensitive-data leakage | Redact payloads and test that logs/events do not expose secrets |

Minimum verifier tests MUST cover tampering, truncation, reordering, replay, forks, crash recovery, key rotation, verification failure, unavailable evidence, and reconstructed legacy events. Tests for a not-yet-approved signature/checkpoint profile are proposals, not proof of production cryptographic security.

## 8. Interoperability example (illustrative only)

This example shows field semantics, not a finalized wire schema or signature format:

```json
{
  "schema_version": "0.1.0",
  "event_id": "evt-example-0007",
  "workflow_id": "wf-example-0012",
  "transition_id": "deploy-admission",
  "sequence": 7,
  "occurred_at": "2026-10-16T18:04:12Z",
  "recorded_at": "2026-10-16T18:04:13Z",
  "actor": {
    "kind": "service",
    "subject": "issuer.example/workload/deployer",
    "identity_evidence": {
      "state": "unverified",
      "reference_id": "identity-evidence-example"
    }
  },
  "action": "release.admit",
  "resource": {
    "type": "deployment",
    "id": "release-example-42"
  },
  "policy": {
    "id": "release-admission",
    "version": "sha256:example-policy-digest"
  },
  "evidence": [
    {
      "type": "test-report",
      "reference_id": "test-report-example",
      "digest_algorithm": "sha256",
      "digest": "example-digest",
      "state": "unverified"
    }
  ],
  "artifacts": [
    {
      "type": "container-image",
      "reference_id": "registry.example/app",
      "digest_algorithm": "sha256",
      "digest": "example-image-digest"
    }
  ],
  "causation_ids": ["evt-example-0006"],
  "correlation_id": "trace-example-9",
  "outcome": "approval_required",
  "failure": null,
  "integrity": null
}
```

All identifiers and digests above are placeholders, not evidence of an actual deployment.

## 9. Adoption gates and open decisions

Before this proposal can become normative, reviewers must decide:

- canonical serialization and cryptographic profile;
- canonical identifier registry and naming conventions;
- authoritative recorder/ledger ownership and append acknowledgement semantics;
- key-management and historical verification policy;
- retention, deletion, legal hold, and privacy rules;
- interoperability requirements and version-compatibility policy;
- test vectors and independent verifier implementation.

No decision above is implied by this proposal. Adoption requires review against GAIA-Documentation #320 and reconciliation with issues #1, #5, #21, #172, and #183. Production integration remains out of scope until separately approved.
