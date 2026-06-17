# OKF Compile Checklist

Use this when generating or updating `okf/`.

## Bundle rules

- Treat `okf/` as an OKF v0.1 Knowledge Bundle derived from `docs/`.
- Keep `docs/` as the source of truth.
- Use one Markdown file per concept.
- The Concept ID is the bundle-relative path without `.md`, for example `modules/parser`.
- `index.md` and `log.md` are reserved names at every directory level and must not be used as concept documents.
- Use standard Markdown links between related concepts.
- Prefer absolute bundle-relative OKF links such as `/modules/parser.md`; relative links are allowed.
- Broken internal links are warnings, not fatal errors.
- Do not introduce new requirements in OKF.

## Index and log rules

- Use `okf/index.md` as the bundle index for progressive disclosure.
- Root `okf/index.md` may declare only `okf_version: "0.1"` in frontmatter.
- Other `index.md` files should not have frontmatter.
- Index entries should be linked list items with short descriptions.
- `log.md` is optional update history.
- Log date headings must use `## YYYY-MM-DD`, newest first.

## Concept page rules

- One page answers one retrieval question.
- Keep pages short.
- Each non-reserved concept file must start with parseable YAML frontmatter.
- Frontmatter must include a non-empty `type` field.
- `type` values are not centrally registered; choose descriptive names and do not reject unknown types.
- Prefer `title`, `description`, `resource`, `tags`, and `timestamp` when useful.
- `tags` should be a YAML list.
- `timestamp` should be an ISO 8601 datetime.
- Include `page_id`, `source_ids`, and `status` as skill-specific extension fields.
- Preserve unknown frontmatter keys when editing.
- Do not copy whole docs sections.

## Body rules

- Use normal Markdown headings, lists, tables, and fenced code blocks.
- Use `# Schema` for structured fields only when the concept describes an asset with fields.
- Use `# Examples` for concrete commands, API calls, or user flows.
- Use `# Citations` for external sources that support claims in the body.
- Use `okf/references/` when external material should be mirrored as first-class OKF concepts.

## Suggested concept skeleton

```md
---
type: Project Requirement
title: <Page Title>
description: <One-sentence retrieval purpose>
tags: [derived, requirement]
timestamp: <ISO 8601 datetime>
page_id: OKF-PAGE-001
source_ids: [URD-REQ-001, ADD-DP-001, MDD-MOD-001]
status: derived
---

# <Page Title>

## What this page answers

## Current facts

## Related concepts

See [related module](/modules/example.md).

## Related IDs

## Do not assume

## Open issues

# Citations

[1] [Source title](https://example.com/source)
```

## Conflict handling

If docs disagree or a source ID is missing, create `okf/issues/PROB-xxxx.md` and route the fix to the right document.
