# URD Discussion Checklist

Use this checklist before writing or updating `docs/URD.md`.

## Ask if unclear

- Who is the primary user?
- What is the one thing the user must be able to accomplish?
- What result proves the project worked?
- What is explicitly out of scope?
- What data is created, stored, modified, or deleted?
- Who can access what?
- What platforms, integrations, and runtime constraints matter?
- What must not happen?

## Do not ask if non-blocking

If a detail does not affect current design, record it as:

- `URD-ASM-xxx` for assumptions
- `URD-Q-xxx` for open questions
- `PARK-xxx` for future ideas

## Exit gate

Move to ADD only when URD has:

- target user
- core task
- success criterion
- in-scope list
- out-of-scope list
- constraints
- assumptions/open questions separated from facts
