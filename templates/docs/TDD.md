# TDD — Test-Driven Document

> Defines executable expectations before implementation.

## Metadata

- document_id: TDD-0001
- status: draft
- source_docs: URD-0001, ADD-0001, MDD-0001
- last_updated:

## Acceptance Tests

| ID | Source AC | Scenario | Given | When | Then | Oracle |
| --- | --- | --- | --- | --- | --- | --- |
| TDD-TEST-001 | URD-AC-001 |  |  |  |  |  |

## Contract Tests

| ID | Interface | Contract Checked | Valid Case | Invalid Case | Oracle |
| --- | --- | --- | --- | --- | --- |
| TDD-TEST-002 | MDD-API-001 | pre/post/invariant |  |  |  |

## Negative / Boundary Tests

| ID | Related Requirement or Interface | Case | Expected Failure |
| --- | --- | --- | --- |
| TDD-TEST-003 |  |  |  |

## Regression Tests

| ID | Protects | Trigger | Oracle |
| --- | --- | --- | --- |
| TDD-TEST-004 | ADD-COUP-001 / DEC-001 |  |  |

## Deferred Tests

| ID | Reason Deferred | Risk | Revisit Trigger |
| --- | --- | --- | --- |
| TDD-TEST-999 |  |  |  |

## TDD Completion Gate

- [ ] Every acceptance criterion maps to a test or explicit deferral.
- [ ] Every public interface has a contract test or explicit reason not to.
- [ ] Invalid inputs and boundary conditions are covered.
- [ ] Accepted coupling has guard tests.
- [ ] Every test has an oracle.
