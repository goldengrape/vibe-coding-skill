# ADD Coupling Retry Checklist

Use this after drafting FRs, DPs, and the design matrix.

## Matrix classification

- Diagonal: uncoupled.
- Triangular: decoupled; record execution order.
- Dense/irregular: coupled; retry before acceptance.

## Retry sequence

1. Split broad FRs.
2. Redefine DPs.
3. Add explicit interfaces, events, adapters, or data boundaries.
4. Move responsibilities between modules.
5. Repeat up to 3 structural retries.

## Accept coupling only if

- coupling remains after retries
- the reason is clear
- risk is recorded
- guard tests are specified
- future refactor trigger is recorded

## Reject fake decoupling

Do not split modules without a real independent responsibility. This creates paperwork and interface noise.
