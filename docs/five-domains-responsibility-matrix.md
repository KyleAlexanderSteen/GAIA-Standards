# Responsibility Matrix: Five Domains

**Status:** Proposed  
**Date:** 2026-10-16  
**Related:** [ADR-001](adr/ADR-001-five-domains-placement.md)

This matrix records what each domain owns, where it lives initially, and what would justify a dedicated repository. It is not a claim that any of these capabilities are implemented.

## Matrix

| Domain | Owns (that existing repos do not) | Initial home | Consumed by | Circular-dependency risk | Dedicated repo justified when |
| --- | --- | --- | --- | --- | --- |
| **Ethics** | Ethical principles, value-conflict analysis, harm criteria, consent and stewardship evaluation tests | GAIA-Standards (normative) + GAIA-Ontology (concepts) | Decision points in Core, agents, and user-facing flows | Low if it only publishes principles and tests | Independently versioned policy set, evaluation engine, or API is required |
| **Law** | Jurisdiction-aware obligations, compliance mappings, regulatory audit evidence requirements | GAIA-Standards (normative) + GAIA-Security (controls) + GAIA-Documentation (references) | Security controls, audit, and release gates | Medium if Law begins to own enforcement | Independent lifecycle, enforcement service, or jurisdiction-specific release cadence is required |
| **Equality** | Non-discrimination criteria, fairness metrics, differential-impact checks | GAIA-Standards (normative) + GAIA-Ontology (concepts) | Evaluation and review processes | Low | Standalone fairness test suite or decision service is required |
| **Coexistence** | Multi-party coordination rules, conflict-containment invariants, shared-resource bounds | GAIA-Standards (normative) + GAIA-Ontology (concepts) | Orchestration and multi-agent flows | Medium if it owns runtime coordination | Runtime coordination logic that cannot live in Core or an orchestrator is required |
| **GAIAN Registry** | Identity, consent, privacy boundary, and registration records for human-linked GAIANs | GAIA-Security (controls) + schema in GAIA-Standards or GAIA-Core | Any component that must resolve a GAIAN identity or consent state | High if the registry also owns ethics or law rules | An actual registration service with its own storage, authentication, and audit is required |

## Distinctions that must be preserved

- Ethics is not Law. An ethical evaluation does not establish legality. Satisfying a legal requirement does not make a decision ethical.
- Equality is not Ethics and not Law. It is a set of measurable non-discrimination and differential-impact criteria.
- Coexistence is not Ethics. It is a set of coordination and containment rules for multiple parties.
- The GAIAN Registry is not an ethics or law document. It is an identity, consent, and registration system. A description of a GAIAN never grants authority over the human.

## Current coverage (not implementation)

| Existing repository | Ethics | Law | Equality | Coexistence | GAIAN Registry |
| --- | --- | --- | --- | --- | --- |
| GAIA-Standards | Partial (can hold normative text) | Partial (can hold normative text) | Partial | Partial | Partial (schema only) |
| GAIA-Ontology | Partial (concepts) | None | Partial (concepts) | Partial (concepts) | None |
| GAIA-Security | None | Partial (controls) | None | None | Partial (controls and audit) |
| GAIA-Core | None | None | None | None | None |
| GAIA-Documentation | Partial (research) | Partial (references) | Partial | Partial | Partial |

"Partial" means the repository can hold related material. It does not mean the material exists or is complete.

## Next step

Review this matrix. For any domain where a concrete capability is blocked, record the blocking capability and re-evaluate the dedicated-repository criteria in ADR-001.
