# Research Evidence and Adoption Gate

**Status:** Proposed standard; not approved.  
**Canonical assessment:** https://github.com/KyleAlexanderSteen/GAIA-Documentation/blob/docs/alignment-attunement-self-improvement/GAIA-Documentation/GAIA-Superintelligence-Architecture-Planetary-Regeneration-and-Engineering-Research-Assessment.md  
**Related existing issues:** GAIA-Documentation #161, #208, #212, #216, #217, #218, #219.

## Purpose

Prevent compelling language, branded frameworks, unverified claims, or generated summaries from becoming GAIA requirements without evidence and explicit review.

## Minimum research record

For each material claim, record:

- Exact claim and scope; whether it is empirical, formal, normative, predictive, or speculative.
- Primary source and version; publication venue and date; access and licensing constraints.
- Independent corroboration, replication status, conflicts of interest, and relevant limitations.
- Assumptions, boundary conditions, counterevidence, alternative explanations, and unknowns.
- Falsifiable predictions and a reproducible validation plan.
- Risk if the claim is wrong, affected repositories/contracts, accountable owner, and approval state.

A citation proves that a source made a claim; it does not prove the claim itself. Multiple secondary pages repeating the same source are not independent corroboration.

## Adoption states

Use explicit states such as **Intake**, **Evidence Review**, **Candidate**, **Pilot Approved**, **Validated for Defined Scope**, **Rejected**, or **Deferred**. Do not collapse these into a single confidence score. Define state-transition criteria and record who authorized each transition.

## Adoption gate

1. Define the problem and measurable outcome.
2. Review primary sources and classify evidence quality.
3. Seek counterevidence and independent replication.
4. Compare with simpler alternatives and existing GAIA capabilities.
5. Define failure modes, privacy/security impact, and rollback.
6. Test in a bounded environment against a baseline.
7. Obtain required human approval before consequential deployment.
8. Record results, limitations, decision, owner, and review date.

## Engineering and AI claims

Terms such as “ASI-ready,” “provably aligned,” “real-time planetary twin,” and numerical failure probabilities require operational definitions and evidence. A theorem prover proves only the encoded statement under stated assumptions. A benchmark score does not establish whole-system safety. A research prototype does not establish production readiness.

## Workflow quality

Issue and PR templates should request the target repository, actionable scope, acceptance criteria, dependencies, evidence, risk, tests, and rollback. Labels such as `llm` may aid routing if the repository actually defines and uses them; do not assume a label alone makes an issue available in a special feed. Code owners and required checks provide enforcement only when correctly configured on the protected base branch.

This proposal is documentation only and does not configure repository rules or approve any technology.