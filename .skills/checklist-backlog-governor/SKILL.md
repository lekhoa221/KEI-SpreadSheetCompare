---
name: checklist-backlog-governor
description: |
    (EN) Coordinate the workflow using a single source of truth (SSOT), the `Checklist & backlog.md` file. Use this for task progress management, mandatory recording and status updates before task execution, proper classification of main checklists vs. auxiliary backlogs, and step-by-step history logging in Vietnamese. Not for bypassing procedures or handling domain-specific code before the checklist update is complete. 
    (VI) Điều phối quy trình làm việc bằng một nguồn sự thật duy nhất (SSOT) là file `Checklist & backlog.md`. Dùng khi cần quản trị tiến độ nhiệm vụ, bắt buộc ghi nhận và cập nhật trạng thái trước khi thực thi task, phân loại đúng checklist chính và backlog phụ trợ, và lưu lịch sử từng bước bằng tiếng Việt. Không dùng để bỏ qua quy trình hoặc xử lý code domain cụ thể khi chưa hoàn tất bước cập nhật checklist.
---

# Checklist Backlog Governor

### Purpose of the Skill

* To establish and enforce a controlled workflow using a single source of truth: `Checklist & backlog.md`.
* To ensure every task leaves a trace: recorded, status updated, and history logged for every significant change.

### When to Use This Skill?

* When coordinating work progress across the entire project.
* When controlling the AI Agent to ensure it only executes tasks after updating the checklist.
* When clearly classifying core development tasks (Checklist) versus auxiliary/trivial tasks (Backlog).
* **Do Not Use:** When attempting to bypass recording procedures or performing ad-hoc work without oversight.

### Operational Workflow (Step-by-Step)

1.  **Mandatory SSOT Gate**
    * Always run the pre-check script:
      `powershell -ExecutionPolicy Bypass -File .skills/checklist-backlog-governor/scripts/ensure_checklist_backlog.ps1 -ProjectRoot .`
    * If `Checklist & backlog.md` does not exist:
        * Treat as a new project.
        * Initialize the file only from the official template.
        * Stop the prompt here and request user review/confirmation before proceeding.

2.  **Pre-Execution Recording**
    * Add tasks to the **Main Checklist** if they are part of the core development flow.
    * Add tasks to the **Auxiliary Backlog** if they involve debugging, minor tweaks, or miscellaneous items.
    * Update the initial status (`TODO` or `DOING`) before modifying any code.

3.  **Execution with Status Updates**
    * Every execution step must reflect a status update in the SSOT file.
    * For every status change, a corresponding entry must be added to the **Change History**.
    * Use the logging script for consistency:
      `powershell -ExecutionPolicy Bypass -File .skills/checklist-backlog-governor/scripts/log_history.ps1 -ProjectRoot . -Entry "..." -Bucket "CHECKLIST" -StepId "CL-001" -Status "DOING"`

4.  **Task Finalization**
    * Mark tasks as `DONE` or `BLOCKED`.
    * Provide a brief reason or outcome in concise Vietnamese.
    * Ensure the user can track the entire workflow simply by opening `Checklist & backlog.md`.

---

### Hard Rules

* [ ] `Checklist & backlog.md` is the **only** SSOT for work progress.
* [ ] No task may be performed if it has not been recorded in the Checklist or Backlog.
* [ ] Every status change **must** be accompanied by a Change History entry.
* [ ] Content within the SSOT file must use concise, easy-to-understand **Vietnamese**.
* [ ] The main development flow and the list of skill components must reside in the **Main Checklist**.
* [ ] Auxiliary work, debugging, and minor adjustments must go into the **Auxiliary Backlog**.

### Soft Rules (Recommendations)

* [ ] Use stable task IDs such as `CL-001`, `BL-001` for easy traceability.
* [ ] Task descriptions should be a single line, focusing strictly on the required outcome.
* [ ] Prefer frequent, small updates over bulk updates at the end of a session.

---

### How to Invoke the Skill (For Users)

* **Implicit (Automatic):**
    * "Use the checklist process to coordinate tasks for this project."
    * "Update the backlog and history before starting this part."
* **Explicit (Forced usage):**
    * `/skills` -> select `checklist-backlog-governor`
    * `$checklist-backlog-governor`

### Dependencies

* **Scripts:**
    * `scripts/ensure_checklist_backlog.ps1` - verifies or initializes the mandatory SSOT file.
    * `scripts/log_history.ps1` - quickly logs a single line into the change history.
* **Reference Documents:**
    * `references/guideline.md` - principles for coordination and classification.
    * `references/checklist.md` - mandatory operational checklist for every session.
* **Template:**
    * `assets/checklist-backlog.template.md` - the standard template for `Checklist & backlog.md`.

### Implementation Notes for Devs

* **Skill Name:** `name` uses lowercase + numbers + hyphens. Folder name must match.
* **Constraints:** Keep `description` concise with clear triggers. Keep `SKILL.md` focused on the process; do not clutter with domain-specific implementation details.

---

### Standardized Self-Test

* Probe token: `SKILL_PROBE_CHECKLIST_BACKLOG_GOVERNOR`
* Expected canary first line: `CANARY_CHECKLIST_BACKLOG_GOVERNOR_OK_20260210`
* Command:
  * `powershell -ExecutionPolicy Bypass -File .skills/run_skill_self_test.ps1 -ProjectRoot . -SkillName checklist-backlog-governor`
* Report file:
  * `temp/skill_probe_checklist-backlog-governor.md`
