# Git Workflow Checklist

Use this checklist after each RMD task or small implementation slice.

## Before coding

- [ ] Main branch is clean.
- [ ] `.gitignore` exists.
- [ ] No secrets or local-only files are staged.
- [ ] The task has one RMD ID.
- [ ] A short feature branch exists for the task.

## Before commit

- [ ] Code changes match one task only.
- [ ] Relevant docs and wiki pages are updated.
- [ ] Tests/checks were run, or failure is recorded.
- [ ] `git status` and `git diff` were reviewed.
- [ ] Commit message includes the RMD task ID.

## Before PR

- [ ] Branch was pushed to the intended remote.
- [ ] PR title is clear.
- [ ] PR body says what changed, how it was tested, affected docs, and known risks.
- [ ] User approved pushing to the remote.

## Before merge

- [ ] Tests/checks pass.
- [ ] User approved merge, or repository rules allow auto-merge.
- [ ] Merge style is recorded in RMD.
- [ ] Feature branch can be deleted after merge.

## Stop immediately if

- A secret, token, password, `.env`, `.venv`, local database, or generated cache appears in the diff.
- Tests fail and the failure is not understood.
- The branch contains changes from multiple unrelated RMD tasks.
