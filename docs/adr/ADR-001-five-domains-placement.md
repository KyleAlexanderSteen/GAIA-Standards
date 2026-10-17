# ADR-001: Placement of Ethics, Law, Equality, Coexistence, and GAIAN Registry

**Status:** Proposed  
**Date:** 2026-10-16  
**Deciders:** Kyle Alexander Steen (human research lead)  
**Context:** GAIA-Standards

## Context

Five domains have been identified as important to GAIA:

1. Ethics
2. Law
3. Equality
4. Coexistence
5. GAIAN Registry

None of these currently have dedicated repositories. The existing architecture already contains GAIA-Standards, GAIA-Ontology, GAIA-Security, GAIA-Core, and related repositories. Creating new repositories before responsibilities, dependencies, and lifecycle needs are defined risks scope expansion and circular dependencies.

## Decision

Do **not** create dedicated repositories for these five domains at this time.

Account for each domain in the architecture now by:

- Defining what it owns that existing repositories do not.
- Recording the initial home (Standards, Ontology, Security, Documentation, or Core).
- Stating the criteria that would later justify a dedicated repository.

A dedicated repository becomes justified only when all of the following are true:

1. The domain requires independent versioning or release cadence.
2. It requires distinct ownership or review process that cannot be satisfied inside an existing repository.
3. It requires implementation (code, tests, or service) that cannot live cleanly inside an existing repository.
4. It has clear consumers and does not create a circular dependency.

## Consequences

- Positive: Completeness is recorded without expanding the repository inventory prematurely.
- Positive: Ethics and Law remain distinct; Equality and Coexistence are not collapsed into either.
- Positive: The GAIAN Registry is treated as an identity-and-consent system, not an ethics document.
- Negative: Some work remains as standards or schemas until a concrete capability forces a split.
- Follow-up: Re-evaluate after the responsibility matrix is reviewed and any concrete capability gap is demonstrated.

## Related

- [Responsibility Matrix](../five-domains-responsibility-matrix.md)
- [GAIAN Registry Requirements](../gaian-registry-requirements.md)
