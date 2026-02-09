---
name: desktop-pyqt-ui-implementation
description: |
  (EN) Implement and review desktop PyQt UI for the Spreadsheet Compare project according to a clear workflow (startup flow, main window layout, result grid interaction, signal-slot wiring, verification). Use when users request to create/edit/refactor/review the desktop interface in `ui/` or `desktop_app.py`, handle widget responsiveness, or optimize operation flow without breaking existing logic. Not for React frontend, backend API, or release deployment workflow. 
  (VI) Triển khai và review giao diện desktop PyQt cho project Spreadsheet Compare theo quy trình rõ ràng (luồng khởi chạy, layout cửa sổ chính, tương tác lưới kết quả, kết nối signal-slot, kiểm chứng). Dùng khi người dùng yêu cầu tạo mới/sửa/refactor/review giao diện desktop trong `ui/` hoặc `desktop_app.py`, xử lý tính linh hoạt của widget, hoặc tối ưu luồng thao tác mà không phá vỡ logic hiện tại. Không dùng cho React frontend, backend API, hoặc quy trình phát hành (release deployment).
---

# Desktop PyQt UI Implementation

### Purpose of the Skill

* The primary objective is to transform desktop interface requirements into structured, testable, and maintainable PyQt code.
* The skill helps reduce UI operation errors, prevent regressions in comparison flows, and maintain code consistency between `desktop_app.py`, `ui/main_window.py`, and `ui/excel/result_view.py`.

### When to Use This Skill?

* **Condition 1:** When the user requests to create new widgets, modify layouts, refactor signal-slot connections, or review the desktop interface.
* **Condition 2:** When the task scope resides within `desktop_app.py`, the `ui/` folder, or core modules directly invoked by the desktop UI.
* **Do Not Use:** When the task involves the React frontend, FastAPI backend, or the publish/update release workflow.

### Operational Workflow (Step-by-Step)

1.  **Requirement Analysis**
    * Identify the request type:
        * [ ] Create New
        * [ ] Modify / Refactor
        * [ ] Review / Verify
        * [ ] Other
    * Clarify the scope: Startup sequence, dashboard, upload flow, comparison flow, result view, or feedback/update prompts.
    * Read minimum context files: `desktop_app.py`, `ui/main_window.py`, `ui/file_drop.py`, and `ui/excel/result_view.py`.

2.  **Preparation / Conditions**
    * Confirm the tech stack:
        * PyQt6 Widgets + Signal/Slot mechanism.
        * `qdarktheme` (light theme).
        * `WorkerThread` for heavy tasks to avoid blocking the UI thread.
    * Run preflight check:
        * `powershell -ExecutionPolicy Bypass -File .skills/desktop-pyqt-ui-implementation/scripts/preflight_desktop_ui.ps1 -ProjectRoot .`
    * For strict verification:
        * `powershell -ExecutionPolicy Bypass -File .skills/desktop-pyqt-ui-implementation/scripts/preflight_desktop_ui.ps1 -ProjectRoot . -VerifyQtImports -RunCompile`

3.  **Core Tasks Execution**
    * Adhere to the rules in `references/guideline.md`.
    * When creating new widgets: Use `assets/pyqt-widget-template.py` as a base.
    * Prioritize minimal necessary changes; maintain existing behaviors and signal contracts.
    * For quick testing: Use `run_desktop.bat`.

4.  **Verification / Optimization**
    * Use the checklist in `references/checklist.md`.
    * **Mandatory Checks:**
        * Loading and error states.
        * Responsiveness during window resizing.
        * State synchronization between `MainWindow` and `ResultView`.
        * Ensure no long-running tasks are executed in the main thread.

---

### Hard Rules

* [ ] Frontmatter must only contain `name` and `description`.
* [ ] **Never block the UI thread** with heavy operations; use `QThread` or appropriate async mechanisms.
* [ ] Do not break existing signal-slot flows unless explicitly requested.
* [ ] Do not change asset loading paths for bundle mode (supporting `sys._MEIPASS`) unless required.
* [ ] Do not modify backend APIs or React frontend code during a desktop UI task unless specified.
* [ ] Do not add new dependencies if the current stack suffices.
* [ ] Add concise comments for complex logic (selection sync, filtering, formula parsing, update flow).

### Soft Rules (Recommendations)

* [ ] Prioritize breaking down `MainWindow` and `ResultView` into smaller functions for easier review.
* [ ] Use meaningful naming conventions for widgets, actions, and signals.
* [ ] Prioritize styling via `objectName` and a central stylesheet over excessive inline styling.
* [ ] Implement **fail-safe UI**: errors must provide clear notifications to the user.

---

### How to Invoke the Skill (For Users)

* **Implicit (Automatic):**
    * "Apply this skill to fix the PyQt desktop interface for the results screen."
    * "Review `ui/main_window.py` according to the skill guidelines."
    * "Refactor the ResultView signal-slot connections for better maintainability."
* **Explicit (Forced usage):**
    * `/skills` -> select `desktop-pyqt-ui-implementation`
    * `$desktop-pyqt-ui-implementation`

### Dependencies

* **Scripts:** `scripts/preflight_desktop_ui.ps1` (verifies conditions before modification/review).
* **Reference Documents:**
    * `references/guideline.md` (PyQt implementation guidelines).
    * `references/checklist.md` (Review and verification checklist).
* **Templates:** `assets/pyqt-widget-template.py` (Widget framework with loading/error state).

### Implementation Notes for Devs

* **Skill Name:** `name` must use lowercase + numbers + hyphens. Folder name must match the `name`.
* **Constraints:** `description` should be concise, clear about triggers, and under 1024 characters. Keep `SKILL.md` under 500 lines.
* **Progressive Disclosure:** Only load reference files when necessary to avoid information overload.