# Document Update Checklist

Use this when a user changes a requirement, design decision, module, interface, test, or implementation path.

1. Identify the source item changed.
2. Locate downstream items in `docs/TRACE.md` and `.vibe/trace.json`.
3. Update the smallest necessary document set.
4. Update affected OKF concept pages.
5. Record the change in `docs/CHANGELOG.md`.
6. Run Ockham check.
7. Run lint.

## Routing examples

- User changes desired behavior: update URD, then ADD/MDD/TDD/RMD as needed.
- Coupling discovered: update ADD first, then MDD/TDD/RMD.
- Interface changes: update MDD, then TDD/RMD/OKF.
- Missing test oracle: update TDD or return to URD if the expected behavior is unclear.
- OKF conflict: create `okf/issues/PROB-xxxx.md`, then fix docs first.
