# GAIA Workflow Provenance Event Contract (Proposal v0.1)

**Status:** Proposed contract for review; not an approved GAIA standard  
**Tracking issue:** [GAIA-Documentation #320](https://github.com/KyleAlexanderSteen/GAIA-Documentation/issues/320)  
**Target repository:** `GAIA-Standards`  
**Change type:** specification  
**Risk level:** medium (normative trust-boundary proposal; no runtime behavior changes)  
**Evidence status:** Derived from the GAIA provenance readiness review; protocol choices below remain proposals pending owner review.

## 1. Purpose and non-goals

Define the minimum event record needed to connect a business-process transition to its actor/workload identity, policy version, evidence, artifact digests, outcome, and causal neighbors. The record is a typed workflow event, not by itself proof that a claim is true, an action is authorized, or an artifact is safe.

This proposal does **not** select a ledger backend, signing library, key-management provider, orchestration engine, or production signing protocol. It does not claim that transport mTLS signs durable workflow events or binds artifact digests. Those require an explicit, independently testable application-level protocol.

## 2. Event record

A conforming implementation proposal must preserve these fields. Field names and the exact wire schema are provisional until registry and interoperability review.

| Field | Required | Semantics |
|---|---:|---|
| `schemaVersion` | yes | Exact event schema version; unknown versions fail verification, not silent coercion. |
| `eventId` | yes | Globally unique stable identifier; never reused for different content. |
| `workflowId` | yes | Stable identifier for the workflow instance. |
| `transitionId` | yes | Stable identifier for this transition attempt. |
| `sequence` | yes | Monotonic sequence within the declared workflow chain; gaps are detectable, not auto-repaired. |
| `occurredAt` | yes | Claimed event time in RFC 3339 UTC form. |
| `recordedAt` | yes | Time the authoritative recorder accepted the event; distinct from occurrence time. |
| `clock` | yes | Clock source/type and known uncertainty, or explicit `unknown`; do not imply precision that is not measured. |
| `actor` | yes | Actor identity reference and identity type; display names alone are insufficient. |
| `workload` | yes | Workload/service identity reference, or explicit `not-applicable` with reason. |
| `action` | yes | Typed action/transition identifier and version. |
| `policy` | yes | Policy identifier, immutable version/digest, and decision reference where applicable. |
| `inputs` | yes | References to input artifacts/evidence with media type, immutable digest, and digest algorithm. Empty inputs must be explicit. |
| `outputs` | yes | Output artifact/evidence references and digests; empty outputs must be explicit. |
| `outcome` | yes | One of `succeeded`, `failed`, `denied`, `cancelled`, or `unknown`; extension requires a versioned schema change. |
| `failure` | conditional | Stable failure code and bounded safe detail when outcome is failed/denied/cancelled/unknown. Secrets and unrestricted payloads are prohibited. |
| `causal` | yes | Parent/trigger event IDs and explicit relation types; roots use an empty list. |
| `trace` | yes | Correlation/trace identifiers for telemetry joins; telemetry is not the authoritative audit record. |
| `evidenceState` | yes | One of `verified`, `reconstructed`, `unverified`, or `disputed`. Reconstruction never silently upgrades to verified. |
| `previousEventDigest` | yes | Digest of the previous event in this chain, or explicit `null` for a declared genesis event. |
| `integrity` | yes | Digest/signature/checkpoint references and verification profile/version; may be pending only before acceptance by an authoritative recorder. |

Implementations must reject missing required fields, unknown outcome/evidence states, malformed digests, duplicate event IDs with differing content, impossible causal self-links, and unsupported schema versions. A valid record can still contain false claims; semantic truth and authorization require separate appraisal.

## 3. Serialization and digest profile

Candidate profile for review:

1. Use UTF-8 JSON with duplicate object keys rejected before parsing into the data model.
2. Evaluate RFC 8785 JSON Canonicalization Scheme (JCS) as the canonical serialization candidate. Pin the exact profile and test vectors before adoption; ordinary JSON stringification is not a cross-implementation canonicalization contract.
3. Compute each event digest over the canonical event payload **excluding** its derived digest/signature fields, with the exact exclusion rule defined in a versioned integrity profile.
4. Include the prior event digest in the payload before computing the current event digest. A verifier checks chain continuity, sequence progression, and event identity.
5. Keep the digest algorithm and profile identifier explicit. Algorithm changes require versioned migration and verification rules; never infer an algorithm from digest length alone.

This is a proposal, not an approved adoption of JCS, a digest algorithm, DSSE, in-toto, or any ledger technology. The implementing workstream must supply golden vectors and independent implementations before a profile is approved.

## 4. Signatures, checkpoints, and key lifecycle

The integrity profile must define, before implementation is treated as verified:

- What exact bytes are signed, the signature envelope/profile version, permitted algorithms, and required signer roles.
- Key ownership and identity binding; creation, activation, rotation, revocation, expiry, compromise handling, and historical verification rules.
- How a verifier obtains trusted key status and distinguishes a missing key from an invalid signature.
- How checkpoints commit to a bounded event range and how independent parties detect divergent forks/equivocation.
- Recovery rules for missing, expired, rotated, or compromised keys. A missing key or unverifiable signature produces a verification failure or explicitly downgraded evidence state; it is never silently accepted.
- Retention and deletion semantics, including how deletion requests interact with append-only commitments and legally required retention.

DSSE/in-toto can be evaluated as candidate attestation components, and PROV-O can describe lineage relationships. They solve different problems and must not be treated as interchangeable. A signature authenticates signed bytes under a key; it does not prove the statement is true or that the signer was authorized for a side effect.

## 5. Telemetry and audit separation

Trace/correlation IDs join operational telemetry to the event record. Telemetry may be sampled, delayed, redacted, or deleted according to its own policy. The authoritative audit/provenance record must not be reconstructed from telemetry without marking the result `reconstructed`.

The event recorder must expose separate outcomes for:
- event validation;
- durable acceptance by the authoritative recorder;
- signature/checkpoint generation;
- downstream telemetry emission.

A telemetry outage must not rewrite an accepted event as absent. Conversely, a successful telemetry write must not be reported as proof that an authoritative event was durably recorded.

## 6. Verification and adversarial test matrix

| Test | Required verifier behavior |
|---|---|
| Payload tampering | Reject digest/signature mismatch. |
| Truncation or missing predecessor | Report incomplete chain; do not infer successful completion. |
| Reordering or sequence gap | Reject or mark chain incomplete with a stable diagnostic. |
| Replay / duplicate event ID | Idempotently recognize byte-identical event; reject conflicting content. |
| Fork / equivocation | Detect conflicting successors or checkpoint roots when compared against the same trusted anchor. |
| Crash between event and checkpoint | Recover without silently skipping accepted events; record explicit pending/recovery state. |
| Key rotation | Verify historical events under the defined historical trust policy and new events under the active policy. |
| Revoked/compromised key | Apply declared compromise time and historical-verification policy; fail closed when trust cannot be established. |
| Unknown schema/profile | Refuse silent downgrade or coercion. |
| Reconstructed legacy event | Preserve `reconstructed` state unless independently re-attested and verified under an approved process. |
| Telemetry outage | Preserve authoritative event state and report telemetry degradation separately. |
| Missing artifact/evidence | Fail the relevant verification claim; do not equate a reference with accessible, digest-matching evidence. |

Tests must include positive and negative golden vectors, property-based or mutation tests where practical, and at least one independent verifier implementation before claiming interoperability.

## 7. Example (illustrative only)

```json
{
  "schemaVersion": "0.1",
  "eventId": "evt-example-0001",
  "workflowId": "wf-example-0001",
  "transitionId": "tr-example-0001",
  "sequence": 0,
  "occurredAt": "2030-01-01T12:00:00Z",
  "recordedAt": "2030-01-01T12:00:01Z",
  "clock": { "source": "example-clock", "uncertaintyMs": 100 },
  "actor": { "id": "actor-ref-1", "type": "service-identity" },
  "workload": { "id": "workload-ref-1", "type": "service" },
  "action": { "id": "example.transition", "version": "1" },
  "policy": { "id": "policy-ref-1", "version": "sha256:example-policy-digest", "decisionRef": "decision-ref-1" },
  "inputs": [],
  "outputs": [],
  "outcome": "succeeded",
  "failure": null,
  "causal": [],
  "trace": { "traceId": "trace-example-1", "correlationId": "corr-example-1" },
  "evidenceState": "unverified",
  "previousEventDigest": null,
  "integrity": { "profile": "pending-review", "digest": null, "signatureRefs": [], "checkpointRef": null }
}
```

The example deliberately uses placeholder references and an unverified state. It is not a production event, a valid signed record, or a normative golden vector.

## 8. Evidence state and release gates

Do not describe this proposal as an approved standard or the event chain as cryptographically verified. Before approval, the work must deliver:

- canonical JSON Schema (or equivalent versioned machine-readable schema);
- a versioned serialization/signature/checkpoint profile and golden vectors;
- a threat model covering tampering, replay, truncation, forks, key compromise, clock uncertainty, privacy leakage, and retention/deletion;
- verifier tests for the matrix above, including recovery and key rotation;
- an interoperability example binding an artifact digest and admission evidence into a deployment/provenance record;
- documented ownership decisions and an explicit list of unresolved items.

**Out of scope for this change:** selecting a ledger backend, signing provider, standard extension, production key management, live deployment/admission integration, or modifying repository visibility/settings.
