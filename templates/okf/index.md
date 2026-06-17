---
okf_version: "0.1"
---

# OKF Bundle Index

> Derived from `docs/`. Do not introduce new requirements here.

# Source Documents

The authoritative project documents live outside this bundle in `docs/`:

- `docs/URD.md` — Idea Brief: user intent, scope, constraints, assumptions, and acceptance criteria.
- `docs/ADD.md` — Design Split: functional requirements, design parameters, and coupling analysis.
- `docs/MDD.md` — Building Blocks: modules, interfaces, contracts, and data structures.
- `docs/TDD.md` — Check Plan: acceptance, contract, negative, boundary, and regression tests.
- `docs/RMD.md` — Build Path: implementation order, stop conditions, rollback points, and Git checkpoints.
- `docs/TRACE.md` — Project Map: links among docs, tasks, tests, and OKF concepts.

OKF pages cite those documents by stable IDs such as `URD-REQ-001` and `MDD-API-001`. Do not link from OKF concept bodies to files outside `okf/` unless a source is intentionally listed under `# Citations`.

# Concept Groups

- [terms](terms/) — Domain terms and abbreviations.
- [requirements](requirements/) — Short pages for important requirements.
- [decisions](decisions/) — Design decisions and tradeoffs.
- [modules](modules/) — Module summaries.
- [interfaces](interfaces/) — Public interfaces and contracts.
- [tests](tests/) — Test oracles and failure cases.
- [paths](paths/) — Implementation routes.
- [issues](issues/) — Contradictions, missing facts, and unresolved questions.
- [references](references/) — Mirrored summaries of external sources cited by concept pages.

# OKF Rules

- `okf/` is an OKF v0.1 Knowledge Bundle derived from `docs/`.
- Every non-reserved `.md` file is a concept document and must have YAML frontmatter with a non-empty `type`.
- Concept IDs are bundle-relative paths without `.md`.
- `index.md` and `log.md` are reserved files, not concepts.
- Prefer bundle-relative links such as `/modules/example.md` inside OKF concept bodies.
- Concept pages reference source IDs instead of copying full source sections.
- If a page conflicts with docs, create `issues/PROB-xxxx.md` and fix docs first.
