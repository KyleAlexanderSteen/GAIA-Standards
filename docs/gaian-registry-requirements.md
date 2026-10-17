# Requirements for a GAIA-GAIAN Registry

**Status:** Proposed  
**Date:** 2026-10-16  
**Related:** [ADR-001](adr/ADR-001-five-domains-placement.md), [Responsibility Matrix](five-domains-responsibility-matrix.md)

## Purpose

A GAIAN Registry would be the system of record for human-linked GAIAN identities, consent state, and registration metadata. It is an identity-and-consent system. It is not an ethics document, a legal code, or an authorization service.

A description or record in the registry must never grant authority over the human.

## What the registry must own

- Registration of a GAIAN identifier linked to a human principal.
- Explicit consent record (who consented, to what, when, and how it can be withdrawn).
- Privacy boundary for the record (what may be read by whom).
- Audit of reads and changes.
- Export and deletion by the human principal.

## What the registry must not own

- Ethical principles or value judgments.
- Legal compliance determinations.
- Authorization decisions beyond "is this record readable/changeable under the stated consent."
- Runtime agent behavior.

## Privacy and consent requirements

These are mandatory before any registry service exists:

1. Explicit consent is required before a record is created.
2. No silent inference of identity from behavior or other data.
3. Least-privilege access: a reader receives only the fields the consent allows.
4. Every read and every change is auditable.
5. The human principal can export their record.
6. The human principal can delete their record; deletion must be recorded.
7. Consent can be withdrawn; withdrawal must stop further use that depended on that consent.
8. A GAIAN description or label never grants authority over the human.

## Initial home (before a dedicated repository)

- Normative requirements and schema: GAIA-Standards
- Controls and audit expectations: GAIA-Security
- Conceptual model of "GAIAN" and "human principal": GAIA-Ontology

## Criteria that would justify a dedicated GAIA-GAIAN repository

All of the following must be true:

1. An actual registration service is required (not only a schema).
2. The service needs its own storage, authentication boundary, and audit log.
3. Independent versioning or release cadence is required.
4. Consumers are identified and no circular dependency is introduced.
5. The service cannot live cleanly inside GAIA-Security or GAIA-Core.

Until those criteria are met, the registry remains a set of requirements and a schema inside existing repositories.

## Non-goals

- No claim that a registry service exists.
- No claim that any GAIAN is registered.
- No use of the registry as a source of authority.
- No mixing of registry records with ethical or legal determinations.
