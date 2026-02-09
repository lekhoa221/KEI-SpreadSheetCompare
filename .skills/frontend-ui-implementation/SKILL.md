---
name: frontend-ui-implementation
description: Implement and review frontend interfaces for React + Vite + Tailwind projects using a controlled workflow (requirement analysis, state/API contract definition, component-based implementation, and lint/build verification). Use this when the user requests to create, modify, refactor, or review the UI, handle responsiveness, or optimize user experience and maintainability without breaking the existing workflow. Not for backend API logic, desktop PyQt UI, or deployment infrastructure changes.
---

# Frontend UI Implementation

### Purpose of the Skill

- The primary goal of this skill is to transform interface requirements into clear, tested, and reviewable frontend code changes.
- It helps save time through a standardized process, checklists, and preflight scripts to minimize errors during UI modifications.

### When to Use This Skill?

- **Condition 1:** When the user requests to create a new screen, modify layouts, refactor components, or review the UI according to guidelines.
- **Condition 2:** When the project utilizes React 18 + Vite + Tailwind located in the `frontend/` directory.
- **Do Not Use:** When the task involves the Python/FastAPI backend, desktop PyQt (`ui/`), or the release/update deployment flow.

### Operational Workflow (Step-by-Step)

1. **Requirement Analysis**
   - Identify the request type:
     - [ ] Create New
     - [ ] Modify / Refactor
     - [ ] Review / Verify
     - [ ] Other
   - Clarify the scope: screens, state management, events, API endpoints, and responsive targets.
   - Read minimum context files:
     - `frontend/src/App.jsx`
     - `frontend/src/components/*.jsx`
     - `frontend/vite.config.js`
     - `frontend/src/index.css`

2. **Preparation / Conditions**
   - Confirm the tech stack:
     - React 18 (hooks + functional components)
     - Vite 7
     - TailwindCSS 3
     - Axios for API calls via `/api` proxy
   - Run preflight:
     - `powershell -ExecutionPolicy Bypass -File .skills/frontend-ui-implementation/scripts/preflight_frontend.ps1 -ProjectRoot .`
   - For strict verification:
     - `powershell -ExecutionPolicy Bypass -File .skills/frontend-ui-implementation/scripts/preflight_frontend.ps1 -ProjectRoot . -RunLint -RunBuild`

3. **Core Tasks Execution**
   - Adhere to the rules in `references/guideline.md`.
   - When creating new components:
     - Use `assets/component-template.jsx` as a base.
   - Prioritize minimal necessary changes, keeping file names and structures consistent with existing code.
   - For API interactions:
     - Maintain existing endpoint contracts (`/api/upload`, `/api/compare`, `/api/sheets/...`, `/api/data/...`) unless a backend change is explicitly requested.

4. **Verification / Optimization**
   - Use the checklist in `references/checklist.md`.
   - Mandatory lint/build checks before concluding major UI tasks.
   - Review:
     - Loading and error states logic.
     - Desktop and mobile responsiveness.
     - Component readability and maintainability.

### Hard Rules

- [ ] Frontmatter must only contain `name` and `description`.
- [ ] Do not change frontend-backend API contracts unless explicitly requested.
- [ ] Do not add new dependencies if the task can be solved with the current stack.
- [ ] Do not modify release/update scripts (`build_app.bat`, `publish_release.bat`) during frontend tasks.
- [ ] Always maintain loading + error states for asynchronous operations (upload, compare, fetch data).
- [ ] Add brief comments for complex or sensitive component logic.

### Soft Rules (Recommendations)

- [ ] Prioritize breaking down large components into smaller, single-responsibility components.
- [ ] Use clear utility classes and maintain consistent colors/spacing.
- [ ] Prioritize reusable helpers for state handling and data transformation.
- [ ] Implement responsive layouts from the start rather than fixing mobile issues at the end.

### How to Invoke the Skill (For Users)

- **Implicit (Automatic):**
  - "Apply this skill to create a new comparison screen for the frontend."
  - "Review the UploadZone component according to the skill guidelines."
  - "Refactor SxSView for better maintainability while keeping current UX."

- **Explicit (Forced usage):**
  - `/skills` -> select `frontend-ui-implementation`
  - `$frontend-ui-implementation`
  - `codex skill frontend-ui-implementation`

### Dependencies

- **Scripts:**
  - `scripts/preflight_frontend.ps1` - verifies frontend conditions before implementation/review.

- **Reference Documents:**
  - `references/guideline.md` - code/UI architecture guidelines for the frontend.
  - `references/checklist.md` - review and verification checklist before handoff.

- **Templates:**
  - `assets/component-template.jsx` - component framework with loading/error/content states.

### Implementation Notes for Devs

- **Skill Name:**
  - `name` must use lowercase + numbers + hyphens (`-`).
  - Folder name must match the `name` value.
- **Constraints:**
  - `description` should be concise, include triggers, and ideally be under 1024 characters.
  - Keep `SKILL.md` lean (under 500 lines); move detailed content to `references/`.
- **Progressive Disclosure:**
  - Only load `references/guideline.md` or `references/checklist.md` when necessary.
  - Avoid duplicating lengthy information between `SKILL.md` and reference files.