# MDD — Module Design Document

> Defines modules, interfaces, contracts, and data structures. Do not repeat URD prose.

## Metadata

- document_id: MDD-0001
- status: draft
- source_add: ADD-0001
- last_updated:

## Module List

| ID | Module | Related DP | Responsibility | Non-Responsibility |
| --- | --- | --- | --- | --- |
| MDD-MOD-001 |  | ADD-DP-001 |  |  |

## Module Dependency Notes

| Module | Depends On | Why | Coupling Risk |
| --- | --- | --- | --- |
| MDD-MOD-001 |  |  | low/medium/high |

## Public Interfaces

| ID | Module | Interface | Inputs | Outputs | Side Effects | Related Tests |
| --- | --- | --- | --- | --- | --- | --- |
| MDD-API-001 | MDD-MOD-001 |  |  |  | none/explicit | TDD-TEST-001 |

## Contracts

| Interface ID | Preconditions | Postconditions | Invariants | Failure Behavior |
| --- | --- | --- | --- | --- |
| MDD-API-001 |  |  |  |  |

## Data Structures

| ID | Used By | Shape / Fields | Mutability | Access Pattern | DOD Justification |
| --- | --- | --- | --- | --- | --- |
| MDD-DATA-001 | MDD-MOD-001 |  | immutable / mutable |  | none / reason |

## Implementation Style Constraints

- Default style:
  - pure functions where practical
  - immutable data unless mutation has a measured or clear reason
  - explicit side effects
- Use data-oriented design only when access pattern, volume, or performance constraints justify it.
- Use contract checks where invalid input or state corruption would be costly.

## MDD Completion Gate

- [ ] Each module maps back to at least one DP.
- [ ] Each module has a narrow responsibility and explicit non-responsibility.
- [ ] Public interfaces have inputs, outputs, side effects, and contracts.
- [ ] Data structures are justified by usage, not by habit.
- [ ] No URD requirement text is repeated unnecessarily.
