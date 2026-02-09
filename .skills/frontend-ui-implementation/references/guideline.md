# Frontend UI Guideline (React + Vite + Tailwind)

## Scope

Use this guideline for implementing or reviewing UI in `frontend/` only.

Current stack:

- React 18 functional components
- Vite dev/build flow
- Tailwind CSS utility-first styling
- Axios calls to backend through `/api` proxy

## Baseline project conventions

1. Keep component structure flat and readable in `frontend/src/components/`.
2. Keep page-level orchestration in `frontend/src/App.jsx` or dedicated view container.
3. Keep async flows explicit: loading, error, and success state.
4. Keep API contract stable unless backend changes are requested.

## Implementation protocol

1. Read existing UI flow before editing:
   - upload
   - compare
   - side-by-side spreadsheet view
2. Define state transitions first:
   - idle
   - loading
   - error
   - ready
3. Implement minimal safe change set.
4. Run lint/build checks after implementation.

## Styling and UX rules

1. Preserve existing visual language unless user requests redesign.
2. Keep contrast readable and interaction states obvious.
3. Ensure layout works on desktop and mobile widths.
4. Avoid over-animating; add motion only when it communicates state.

## Review focus

During review, prioritize:

1. Regressions in upload/compare flows.
2. Broken async state handling.
3. Layout breakpoints and overflow issues.
4. Duplicated logic that should be extracted.
