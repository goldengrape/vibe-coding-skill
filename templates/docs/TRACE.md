# TRACE — Project Map / Traceability

> Human-readable trace index. Machine-readable copy lives in `.vibe/trace.json`.

## Trace Chains

| Source ID | Relation | Target ID / Path | Notes |
| --- | --- | --- | --- |
| URD-REQ-001 | refines_to | ADD-FR-001 |  |
| ADD-FR-001 | satisfied_by | ADD-DP-001 |  |
| ADD-DP-001 | implemented_by | MDD-MOD-001 |  |
| MDD-MOD-001 | exposes | MDD-API-001 |  |
| MDD-API-001 | verified_by | TDD-TEST-001 |  |
| TDD-TEST-001 | scheduled_in | RMD-TASK-001 |  |
| RMD-TASK-001 | summarized_by | wiki/paths/example.md |  |
| RMD-SETUP-001 | precedes | RMD-TASK-001 | project setup before feature work |
| RMD-SETUP-002 | precedes | RMD-TASK-001 | uv package setup for Python projects |
| RMD-TASK-001 | checkpointed_by | RMD-GIT-001 | every completed slice should have a Git checkpoint |
| RMD-GIT-001 | reviewed_by | RMD-PR-001 | use PR when a remote exists |

## Orphan Items

Items listed here need either a trace link or removal.

| ID | Found In | Action |
| --- | --- | --- |

## Trace Update Rule

When URD, ADD, MDD, TDD, RMD, or wiki changes, update this file and `.vibe/trace.json` in the same commit/change set.
