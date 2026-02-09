# Backend API Checklist

## Pre-implementation

- [ ] Confirm endpoint scope and expected request and response shape.
- [ ] Identify impacted routers and core modules.
- [ ] Run backend preflight script.

## Implementation

- [ ] Keep router function focused on HTTP orchestration.
- [ ] Move reusable processing logic to `backend/core`.
- [ ] Validate request payload with Pydantic model where appropriate.
- [ ] Map predictable failures to clear HTTP status codes.
- [ ] Keep response keys compatible with frontend expectations.

## Verification

- [ ] Run compile check for backend Python files.
- [ ] Run tests if available.
- [ ] Manually verify key flows:
  - upload
  - compare
  - sheets listing
  - sheet data retrieval
  - analyze
- [ ] Verify error scenarios (missing file, invalid input, dependency failure).

## Handoff

- [ ] Summarize assumptions and potential side effects.
- [ ] List changed files and why.
- [ ] Capture follow-up tasks if technical debt remains.
