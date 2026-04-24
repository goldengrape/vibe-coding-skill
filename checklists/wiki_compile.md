# Wiki Compile Checklist

Use this when generating or updating `wiki/`.

## Page rules

- One page answers one retrieval question.
- Keep pages short.
- Link to source IDs.
- Do not copy whole docs sections.
- Do not introduce new requirements.

## Suggested page skeleton

```md
# <Page Title>

- page_id: WIKI-PAGE-001
- source_ids: URD-REQ-001, ADD-DP-001, MDD-MOD-001
- status: derived

## What this page answers

## Current facts

## Related IDs

## Do not assume

## Open issues
```

## Conflict handling

If docs disagree or a source ID is missing, create `wiki/issues/PROB-xxxx.md` and route the fix to the right document.
