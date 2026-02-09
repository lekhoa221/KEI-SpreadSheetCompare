# Backend API Guideline (FastAPI)

## Scope

Use this guideline for backend API work inside `backend/`.

Current structure:

- `backend/main.py` for app bootstrap and router registration
- `backend/routers/` for HTTP endpoints
- `backend/core/` for business logic and data processing

## API contract baseline

Keep these endpoints stable unless explicitly asked to change them:

1. `POST /api/upload`
2. `POST /api/compare`
3. `GET /api/sheets/{filename}`
4. `GET /api/data/{filename}/{sheet_name}`
5. `POST /api/analyze`

## Implementation protocol

1. Clarify input and output schema first.
2. Add or update Pydantic models for request validation.
3. Keep router handlers thin; call helper functions in core modules.
4. Convert unexpected errors into explicit HTTP errors with actionable detail.
5. Re-check frontend dependency on response fields before renaming keys.

## Error handling rules

1. Use `HTTPException` with appropriate status code.
2. Return clear details for file-not-found, invalid payload, and processing failures.
3. Avoid exposing internal stack traces in responses.
4. Log or preserve enough detail for debugging in development mode.

## Data and file safety

1. Validate file path inputs before processing.
2. Keep temp file operations isolated in backend temp directory.
3. Avoid mutating source files during comparison flow.
4. Guard large-file operations and external service calls with timeouts where possible.

## Review focus

Prioritize these checks:

1. Contract compatibility with frontend.
2. Validation coverage and schema correctness.
3. Error-path behavior and status codes.
4. Separation of concerns between router and core modules.
