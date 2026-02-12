---
name: update-release-workflow
description: |
  (EN) Standardize, implement, and review secure update release flows for Python desktop applications in a LAN environment (build, package.zip, version.json, publish, LATEST.txt, updater). Use for managing version/hash mismatches, rollback procedures, or release checklists. Not for cloud/internet-first CI/CD or non-release tasks.
  (VI) Chuẩn hóa, triển khai, và review luồng update release an toàn cho ứng dụng desktop Python trong LAN (build, package.zip, version.json, publish, LATEST.txt, updater). Dùng khi người dùng yêu cầu tạo mới/sửa/refactor/review quy trình cập nhật, xử lý mismatch version/hash, hoặc thiết lập checklist phát hành. Không dùng cho cloud deployment, CI/CD internet-first.
---

# Update Release Workflow

### Purpose of the Skill

* The primary objective is to transform "update version" requests into a controlled, repeatable release process.
* The skill helps **minimize publishing errors**, ensures consistent versioning, and shortens release cycles through standardized checklists and preflight scripts.

### When to Use This Skill?

* **Condition 1:** When the user requests to create, modify, or review update flows, version releases, rollbacks, or update error debugging.
* **Condition 2:** When the project is a Python desktop application (PyInstaller) distributed via LAN shares using `LATEST.txt` and a `releases/<version>/` structure.
* **Do Not Use:** For cloud deployments, container orchestration, mobile OTA updates, or vague requests unrelated to the release lifecycle.

### Operational Workflow (Step-by-Step)

1.  **Requirement Analysis**
    * Identify the request type:
        * [ ] Create New
        * [ ] Modify / Refactor
        * [ ] Review / Verify
        * [ ] Other
    * Determine the impact scope: build/publish scripts, updater logic, release documentation, or just the checklist.
    * Read minimum context files: `VERSION.txt`, `publish_release.bat`, `build_app.bat`, `core/update_manager.py`, and `docs/UPDATE_WORKFLOW.md`.

2.  **Preparation / Conditions**
    * Confirm the environment and tech stack:
        * Python + PyInstaller.
        * Batch/PowerShell on Windows.
        * LAN share root (`REMOTE_ROOT`) and local release root (`releases/`).
    * Run preflight check before publishing:
      `powershell -ExecutionPolicy Bypass -File .skills/update-release-workflow/scripts/preflight_update.ps1 -ProjectRoot .`
    * If the release requires a formal installer:
      `powershell -ExecutionPolicy Bypass -File .skills/update-release-workflow/scripts/preflight_update.ps1 -ProjectRoot . -RequireInstaller`

3.  **Core Tasks Execution**
    * Adhere to the release protocol in `references/guideline.md`.
    * **Full Release Sequence:**
        1. Run `build_app.bat`
        2. Run `build_installer.bat` (if applicable)
        3. Run `publish_release.bat`
    * **Quick Local Update Test:** Follow `docs/quick_update_test.md` for rapid testing without full rebuild loops.
    * If creating new manifests: Use `assets/version.json.template`.
    * For reviews: Use the checklist in `references/checklist.md` and mark items as pass/fail.

4.  **Verification / Optimization**
    * Ensure version consistency across `VERSION.txt`, `dist/AppName/VERSION.txt`, and `version.json`.
    * Verify file hashes and package metadata in `version.json`.
    * **Crucial Sequencing:** Upload `package.zip` + `version.json` + updater files **before** updating `LATEST.txt` to prevent "partial update" errors.
    * Propose improvements if anti-patterns are detected, but do not modify sensitive config files without explicit approval.



---

### Hard Rules

* [ ] Frontmatter must only contain `name` and `description`.
* [ ] **Single Source of Truth:** Use `VERSION.txt` as the primary version reference; all other version points must synchronize with it.
* [ ] **`LATEST.txt` Update:** This must be the **final step** in the publishing process.
* [ ] **Integrity Checks:** If using `package.zip`, both `sha256` and `size` in `version.json` are mandatory.
* [ ] Do not modify critical configuration files (`setup.iss`, `installer/version.iss`, release root paths) unless explicitly requested.
* [ ] Do not introduce new dependencies unless there is a mandatory technical requirement.
* [ ] Add concise comments for complex logic (version parsing, rollback mechanisms, copy-retry loops).

### Soft Rules (Recommendations)

* [ ] Prioritize modularizing update logic into small, testable, and reversible functions.
* [ ] Use existing scripts (`build_app.bat`, `publish_release.bat`) rather than manual CLI commands.
* [ ] **Fail-fast:** Detect version/hash mismatches locally before attempting to copy to the remote LAN share.
* [ ] **Idempotent Updates:** Ensure the publishing script can be re-run without breaking an existing release.

---

### How to Invoke the Skill (For Users)

* **Implicit (Automatic):**
    * "Apply this skill to standardize the LAN update publishing process."
    * "Review the current update flow and create a pre-release checklist."
    * "Modify the publish script to safely update `LATEST.txt`."
* **Explicit (Forced usage):**
    * `/skills` -> select `update-release-workflow`
    * `$update-release-workflow`

### Dependencies

* **Scripts:** `scripts/preflight_update.ps1` (pre-build/publish verification).
* **Reference Documents:**
    * `references/guideline.md` (LAN-specific release/update guidelines).
    * `references/checklist.md` (Pre-release, post-release, and rollback checklists).
* **Templates:** `assets/version.json.template` (JSON manifest for version metadata).

### Implementation Notes for Devs

* **Skill Name:** `name` must be lowercase + numbers + hyphens. Folder name must match.
* **Constraints:** Keep `description` under 1024 characters. Keep `SKILL.md` focused on the workflow; move detailed documentation to `references/`.
* **Progressive Disclosure:** Only load reference files when strictly necessary to manage context window efficiency.

---

### Standardized Self-Test

* Probe token: `SKILL_PROBE_UPDATE_RELEASE_WORKFLOW`
* Expected canary first line: `CANARY_UPDATE_RELEASE_WORKFLOW_OK_20260210`
* Command:
  * `powershell -ExecutionPolicy Bypass -File .skills/run_skill_self_test.ps1 -ProjectRoot . -SkillName update-release-workflow`
* Report file:
  * `temp/skill_probe_update-release-workflow.md`
