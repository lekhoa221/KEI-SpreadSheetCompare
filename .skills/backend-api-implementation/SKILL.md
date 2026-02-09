---
name: backend-api-implementation
description: |
  (EN) Implement and review backend APIs for the Spreadsheet Compare FastAPI project using a clear workflow (router design, validation, error handling, integration with core modules, verification). Use when users request to create/edit/refactor/review API endpoints, handle upload/compare/sheets/analyze flows, or standardize the frontend-backend contract. Not for frontend UI implementation, desktop PyQt UI, or release deployment workflow.

  (VI) Triển khai và review backend API cho project FastAPI của Spreadsheet Compare theo quy trình rõ ràng (router design, validation, error handling, tích hợp với core modules, kiểm chứng). Dùng khi người dùng yêu cầu tạo mới/sửa/refactor/review endpoint API, xử lý luồng upload/compare/sheets/analyze, hoặc chuẩn hóa contract giữa frontend và backend. Không dùng cho frontend UI implementation, desktop PyQt UI, hoặc quy trình phát hành (release deployment).
---

# Backend API Implementation

### Purpose of the Skill

* The primary goal is to transform API requirements into structured, secure, and maintainable FastAPI backend changes.
* This skill helps minimize frontend-backend contract mismatches, reduce regressions in upload/compare flows, and accelerate the review process while maintaining high quality.

### When to Use This Skill?

* **Condition 1:** When the user requests to create new endpoints, modify routers, refactor service logic, or review the backend.
* **Condition 2:** When the project uses FastAPI with the structure: `backend/main.py`, `backend/routers/`, and `backend/core/`.
* **Do Not Use:** When the task primarily involves the React frontend, desktop PyQt UI, or the publish/update release workflow.

### Operational Workflow (Step-by-Step)

1.  **Requirement Analysis**
    * Identify the request type:
        * [ ] Create New
        * [ ] Modify / Refactor
        * [ ] Review / Verify
        * [ ] Other
    * Clarify affected endpoints, request/response schemas, and business logic changes.
    * Read minimum context files: `backend/main.py`, `backend/routers/*.py`, `backend/core/*.py`, and `backend/requirements.txt`.

2.  **Preparation / Conditions**
    * Confirm the tech stack:
        * FastAPI + Uvicorn.
        * Pydantic models for request validation.
        * Pandas and OpenPyXL for Excel processing.
        * Ollama for AI analysis endpoints.
    * Run preflight check:
        * `powershell -ExecutionPolicy Bypass -File .skills/backend-api-implementation/scripts/preflight_backend.ps1 -ProjectRoot .`
    * For strict verification after major changes:
        * `powershell -ExecutionPolicy Bypass -File .skills/backend-api-implementation/scripts/preflight_backend.ps1 -ProjectRoot . -RunCompile -RunPytest`

3.  **Core Tasks Execution**
    * Adhere to rules in `references/guideline.md`.
    * Prioritize placing HTTP logic in **routers** and data processing logic in `backend/core`.
    * Preserve existing endpoint contracts unless a change is explicitly requested:
        * `POST /api/upload`
        * `POST /api/compare`
        * `GET /api/sheets/{filename}`
        * `GET /api/data/{filename}/{sheet_name}`
        * `POST /api/analyze`
    * If creating a new endpoint: Use `assets/router-template.py` as a base.

4.  **Verification / Optimization**
    * Use the checklist in `references/checklist.md`.
    * **Check Error Handling for:**
        * File not found.
        * Incorrect payload format.
        * I/O errors.
        * Dependency service failures (e.g., Ollama).
    * Ensure status codes and error messages are consistent for stable frontend handling.

---

### Hard Rules

* [ ] Frontmatter must only contain `name` and `description`.
* [ ] **Do not break existing API contracts** without an explicit requirement.
* [ ] Do not bypass request validation for endpoints that write or process data.
* [ ] **Never swallow exceptions silently**; map them to appropriate `HTTPException` responses.
* [ ] Do not add new dependencies if the current stack meets the requirements.
* [ ] Do not modify build/publish scripts during a backend API task unless requested.
* [ ] Add concise comments for complex logic that isn't self-documenting.

### Soft Rules (Recommendations)

* [ ] Prioritize breaking logic into small, testable functions within `backend/core`.
* [ ] Use meaningful naming conventions for routers, models, and helper functions.
* [ ] Prioritize **fail-fast** logic and consistent error messaging.
* [ ] Maintain stable response shapes to prevent breaking the frontend.

---

### How to Invoke the Skill (For Users)

* **Implicit (Automatic):**
    * "Apply this skill to create a new backend endpoint."
    * "Review the backend routers according to the skill guidelines."
    * "Refactor the compare API flow for better maintainability."
* **Explicit (Forced usage):**
    * `/skills` -> select `backend-api-implementation`
    * `$backend-api-implementation`

### Dependencies

* **Scripts:** `scripts/preflight_backend.ps1` (verifies backend conditions before modification/review).
* **Reference Documents:**
    * `references/guideline.md` (Backend API implementation guidelines).
    * `references/checklist.md` (Pre-handoff checklist).
* **Templates:** `assets/router-template.py` (FastAPI router framework with request models and error handling).

### Implementation Notes for Devs

* **Skill Name:** `name` must use lowercase + numbers + hyphens. Folder name must match.
* **Constraints:** Keep `description` concise with clear triggers. Keep `SKILL.md` under 500 lines; move detailed content to `references/`.
* **Progressive Disclosure:** Only load reference files when necessary.