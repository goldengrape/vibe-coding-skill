# RMD — Route / Runbook / Execution Map Document

> Defines implementation order, stop conditions, rollback points, and Git checkpoints.

Beginner name: Build Path.

## Metadata

- document_id: RMD-0001
- status: draft
- source_docs: URD-0001, ADD-0001, MDD-0001, TDD-0001
- last_updated:

## Project Setup

| ID | Item | Decision | Command / File | Done When |
| --- | --- | --- | --- | --- |
| RMD-SETUP-001 | stack | Python / other |  | stack chosen and recorded |
| RMD-SETUP-002 | package manager | uv for Python | `uv init --app .` or `uv init --lib .` | `pyproject.toml` exists |
| RMD-SETUP-003 | ignore rules | create `.gitignore` | `.gitignore` | generated files and secrets ignored |
| RMD-SETUP-004 | tests folder | create initial test location | `tests/` | test command can run |
| RMD-SETUP-005 | git repository | initialize or verify repo | `git status` | clean starting state |

## Execution Strategy

- strategy:
- risk posture: simple | standard | strict
- first implementation slice:
- default branch: main
- merge style: squash | merge commit | rebase

## Ordered Tasks

| ID | Task | Depends On | Inputs | Outputs | Test / Check Command | Branch | Done When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RMD-TASK-001 |  |  | URD/ADD/MDD/TDD IDs |  | `uv run pytest` | `feat/rmd-task-001-short-name` | tests pass / docs updated / commit created |

## 🔴 Git Checkpoints

Every task should end with a checkpoint unless git is explicitly disabled. First push and first merge require explicit approval.

| ID | RMD Task | Branch | Commit Message | PR | Merge Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| RMD-GIT-001 | RMD-TASK-001 | `feat/rmd-task-001-short-name` | `feat: implement RMD-TASK-001 short name` | pending / opened / skipped | pending / merged / skipped |  |

### Checkpoint Procedure

```bash
git checkout main
git pull --ff-only
git checkout -b feat/rmd-task-001-short-name
# implement one small slice
uv run pytest
uv run ruff check .
git status
git diff
git add <changed-files>
git commit -m "feat: implement RMD-TASK-001 short name"
git push -u origin feat/rmd-task-001-short-name
gh pr create --fill
```

Merge only after tests/checks pass and user or repository rules approve. Do not push or merge from a dirty working tree.

## 🛑 Stop Conditions

| ID | Condition | Action |
| --- | --- | --- |
| RMD-STOP-001 | unresolved blocking URD question | return to URD |
| RMD-STOP-002 | ADD coupling violation without accepted coupling record | return to ADD |
| RMD-STOP-003 | missing test oracle | return to TDD |
| RMD-STOP-004 | no clean git state before implementation | pause and inspect changes |
| RMD-STOP-005 | tests/checks fail before commit or merge | fix or route back to MDD/TDD |
| RMD-STOP-006 | secret or local-only file appears in git diff | remove from git and update `.gitignore` |
| RMD-STOP-007 | first push, merge, deletion, or overwrite is needed | stop for explicit approval |

## Rollback Points

| ID | After Step | Rollback Action |
| --- | --- | --- |
| RMD-RB-001 | project initialized | revert setup commit or restore previous branch |
| RMD-RB-002 | interface stubs created | revert stubs and update MDD |
| RMD-RB-003 | task branch pushed | close PR without merge or revert commit |
| RMD-RB-004 | PR merged | create revert PR and update CHANGELOG |

## RMD Completion Gate

- [ ] Tasks are ordered by dependency and risk.
- [ ] Project setup is complete before feature implementation.
- [ ] `.gitignore` exists before the first commit.
- [ ] Python projects use `uv` unless a reason is recorded.
- [ ] Interface stubs and failing tests come before implementation where practical.
- [ ] Every task has a test/check command.
- [ ] Every completed task has a Git checkpoint or a recorded reason for skipping it.
- [ ] PR and merge status are recorded for remote repositories.
- [ ] Stop conditions route back to the correct document.
- [ ] Rollback points exist at risky boundaries.
