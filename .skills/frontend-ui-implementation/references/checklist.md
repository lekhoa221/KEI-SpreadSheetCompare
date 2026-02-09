# Frontend UI Checklist

## Pre-implementation

- [ ] Confirm target scope (new screen, refactor, review, or bug fix).
- [ ] Identify impacted components and API calls.
- [ ] Run preflight script before major edits.

## Implementation

- [ ] Keep loading, error, and success states explicit.
- [ ] Keep component responsibilities narrow and clear.
- [ ] Avoid unnecessary global state.
- [ ] Keep API endpoints unchanged unless required.
- [ ] Ensure Tailwind classes remain readable and consistent.

## Verification

- [ ] Run lint (`npm run lint`).
- [ ] Run build (`npm run build`).
- [ ] Verify upload -> compare -> side-by-side flow manually.
- [ ] Verify responsive behavior on narrow and wide screens.
- [ ] Verify error message paths for API failures.

## Handoff

- [ ] Document assumptions and known limitations.
- [ ] List files changed and rationale.
- [ ] Note follow-up tasks if debt remains.
