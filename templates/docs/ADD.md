# ADD — Axiomatic Design Document

> Maps Functional Requirements (FRs) to Design Parameters (DPs). Detects coupling before coding.

## Metadata

- document_id: ADD-0001
- status: draft
- source_urd: URD-0001
- last_updated:

## Functional Requirements

| ID | Source | Functional Requirement | Notes |
| --- | --- | --- | --- |
| ADD-FR-001 | URD-REQ-001 / URD-AC-001 |  |  |

## Design Parameters

| ID | Satisfies FR | Design Parameter | Rationale |
| --- | --- | --- | --- |
| ADD-DP-001 | ADD-FR-001 |  |  |

## FR / DP Design Matrix

Use `X` where a DP affects an FR. Prefer diagonal. Accept triangular only when execution order is clear.

| FR \ DP | ADD-DP-001 |
| --- | --- |
| ADD-FR-001 | X |

## Matrix Classification

- classification: uncoupled | decoupled | coupled
- reason:
- execution_order_if_decoupled:

## Coupling Retry Log

| Attempt | Problem | Change Made | Result |
| --- | --- | --- | --- |
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |

## 🛑 Accepted Coupling

Use only when coupling remains after retries and is justified. Implementation must not start until this section is complete for any unresolved coupling.

| ID | Coupled FRs | Coupled DPs | Reason | Risk | Guard Tests | Refactor Trigger |
| --- | --- | --- | --- | --- | --- | --- |
| ADD-COUP-001 |  |  |  |  |  |  |

## ADD Completion Gate

- [ ] Every confirmed URD requirement that affects behavior has at least one FR or is explicitly deferred.
- [ ] Every FR has a DP.
- [ ] Design matrix is present.
- [ ] Coupling classification is explicit.
- [ ] Coupled designs have up to 3 retry records before acceptance.
- [ ] Accepted coupling has risk and guard tests.
- [ ] No meaningless module split was introduced just to improve the matrix.
