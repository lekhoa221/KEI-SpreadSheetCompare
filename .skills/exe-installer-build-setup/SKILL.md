---
name: exe-installer-build-setup
description: |
  Set up and review the EXE build and installer build workflow for a Windows desktop Python app (PyInstaller and Inno Setup), including preflight checks, version sync, artifact validation, and mismatch handling. Use when users ask to create, modify, refactor, or review build_app.bat, build_installer.bat, setup.iss, or local build pipeline behavior. Do not use for LAN release publishing, frontend implementation, or backend API implementation.
---

# Exe Installer Build Setup

### Purpose

- Standardize the `.exe` and installer build pipeline so it is repeatable and predictable.
- Reduce build failures caused by version mismatch, missing artifacts, and incorrect Inno Setup configuration.

### When to use this skill

- Condition 1: The user asks to set up, modify, or review EXE and installer build workflows.
- Condition 2: The project uses `build_app.bat`, `build_installer.bat`, `setup.iss`, and `installer/version.iss`.
- Do not use: The task is about LAN release publishing, frontend UI, backend API, or runtime desktop behavior unrelated to build.

### Workflow (step-by-step)

1. **Analyze the request**
   - Classify the request:
     - [ ] Create new
     - [ ] Modify / refactor
     - [ ] Review / verify
     - [ ] Other
   - Identify build scope:
     - EXE build
     - installer build
     - or both
   - Read minimum context:
     - `build_app.bat`
     - `build_installer.bat`
     - `setup.iss`
     - `VERSION.txt`

2. **Prepare prerequisites**
   - Run preflight:
     - `powershell -ExecutionPolicy Bypass -File .skills/exe-installer-build-setup/scripts/preflight_build_pipeline.ps1 -ProjectRoot .`
   - For stricter checks:
     - `powershell -ExecutionPolicy Bypass -File .skills/exe-installer-build-setup/scripts/preflight_build_pipeline.ps1 -ProjectRoot . -RequireBuildOutput -RequireInnoSetup`
   - Confirm version strategy:
     - `build_app.bat` auto-bumps the patch version.

3. **Execute main tasks**
   - Build EXE:
     - `build_app.bat`
   - Build installer:
     - `build_installer.bat`
   - If needed, use the menu wrapper:
     - `run_tasks.bat` and choose relevant options.

4. **Verify and optimize**
   - Validate expected outputs:
     - `dist/DocCompareAI/DocCompareAI.exe`
     - `updater/Updater.exe`
     - `installer/DocCompareAI_Setup_v<version>.exe`
   - Validate version consistency:
     - `VERSION.txt`
     - `installer/version.iss`
     - installer output filename
   - Summarize results using `assets/installer-build-report.template.md`.

### Hard rules

- [ ] Frontmatter must contain only `name` and `description`.
- [ ] Do not build installer if `dist/DocCompareAI/DocCompareAI.exe` is missing.
- [ ] Do not modify `setup.iss` unless explicitly requested.
- [ ] Do not change release/publish scripts for build-only tasks.
- [ ] Always account for patch auto-bump in `build_app.bat`.
- [ ] Do not add new dependencies unless strictly necessary.

### Soft rules

- [ ] Prefer running preflight before any build.
- [ ] Prefer fail-fast behavior for missing Inno Setup, missing output, or version mismatch.
- [ ] Prefer writing a short build summary after significant build runs.

### How to invoke

- **Implicit (automatic):**
  - "Apply this skill to set up EXE and installer build flow."
  - "Review build_app.bat and build_installer.bat based on the skill guideline."

- **Explicit (forced):**
  - `/skills` -> choose `exe-installer-build-setup`
  - `$exe-installer-build-setup`
  - `codex skill exe-installer-build-setup`

### Skill resources

- Scripts:
  - `scripts/preflight_build_pipeline.ps1` - preflight checks for EXE and installer build conditions.

- References:
  - `references/guideline.md` - build pipeline protocol and rules.
  - `references/checklist.md` - pre, during, and post-build checklist.

- Template:
  - `assets/installer-build-report.template.md` - build result summary template.

### Implementation notes

- Skill naming:
  - `name` uses lowercase letters, digits, and hyphens.
  - Folder name must match `name`.

- Limits:
  - Keep `description` concise and trigger-oriented (prefer under 1024 chars).
  - Keep `SKILL.md` concise (prefer under 500 lines), move details to `references/`.

---

### Standardized Self-Test

- Probe token: `SKILL_PROBE_EXE_INSTALLER_BUILD_SETUP`
- Expected canary first line: `CANARY_EXE_INSTALLER_BUILD_SETUP_OK_20260210`
- Command:
  - `powershell -ExecutionPolicy Bypass -File .skills/run_skill_self_test.ps1 -ProjectRoot . -SkillName exe-installer-build-setup`
- Report file:
  - `temp/skill_probe_exe-installer-build-setup.md`
