---
name: publish-release-workflow
description: |
  Set up and review the release publish workflow for this project, including package creation, hash generation, manifest writing, remote copy, and safe latest-version switching. Use when users ask to create, modify, refactor, or verify publish_release.bat behavior and release artifact integrity. Do not use for EXE or installer build implementation itself, frontend work, backend API work, or desktop UI implementation.
---

# Publish Release Workflow

### Purpose

- Standardize publish operations so artifacts are complete, verifiable, and safe to switch live.
- Reduce failures caused by missing package files, hash mismatches, installer mismatch, and incorrect publish ordering.

### When to use this skill

- Condition 1: The user asks to set up, modify, or review release publish flow.
- Condition 2: The task targets `publish_release.bat`, release folder structure, `version.json`, and remote publish checks.
- Do not use: The task is pure EXE build or installer build setup (use the build skill for that).

### Workflow (step-by-step)

1. **Analyze request**
   - Classify request:
     - [ ] Create new
     - [ ] Modify / refactor
     - [ ] Review / verify
     - [ ] Other
   - Identify scope:
     - local release packaging only
     - remote publish only
     - or full publish pipeline
   - Read minimum context:
     - `publish_release.bat`
     - `VERSION.txt`
     - `docs/UPDATE_WORKFLOW.md`

2. **Prepare prerequisites**
   - Run preflight:
     - `powershell -ExecutionPolicy Bypass -File .skills/publish-release-workflow/scripts/preflight_publish_release.ps1 -ProjectRoot .`
   - For strict publish checks:
     - `powershell -ExecutionPolicy Bypass -File .skills/publish-release-workflow/scripts/preflight_publish_release.ps1 -ProjectRoot . -RequireInstaller -RequireRemoteRoot`

3. **Execute publish tasks**
   - Default publish:
     - `publish_release.bat`
   - Fast local test publish (no installer check):
     - `set SKIP_INSTALLER_CHECK=1`
     - `publish_release.bat`
   - Confirm artifact outputs:
     - `releases/<version>/package.zip`
     - `releases/<version>/version.json`
     - optional `releases/<version>/updater/Updater.exe`

4. **Verify and optimize**
   - Validate package hash and size in `version.json`.
   - Validate publish ordering:
     - copy artifacts first
     - update `LATEST.txt` last
   - Summarize results using `assets/publish-release-report.template.md`.

### Hard rules

- [ ] Frontmatter must contain only `name` and `description`.
- [ ] Do not publish if `dist/DocCompareAI/DocCompareAI.exe` is missing.
- [ ] Always write and validate `version.json` metadata for package path, hash, and size.
- [ ] Update `LATEST.txt` only after all release artifacts are uploaded.
- [ ] Do not modify unrelated build or runtime files unless explicitly requested.

### Soft rules

- [ ] Run preflight before publish tasks.
- [ ] Prefer fail-fast checks for version mismatch and missing installer.
- [ ] Keep publish summaries short and consistent for traceability.

### How to invoke

- **Implicit (automatic):**
  - "Apply this skill to set up release publishing."
  - "Review publish_release.bat and release packaging flow."

- **Explicit (forced):**
  - `/skills` -> choose `publish-release-workflow`
  - `$publish-release-workflow`
  - `codex skill publish-release-workflow`

### Skill resources

- Scripts:
  - `scripts/preflight_publish_release.ps1` - preflight checks for release publish readiness.

- References:
  - `references/guideline.md` - publish protocol and safety rules.
  - `references/checklist.md` - pre, during, and post-publish checklist.

- Template:
  - `assets/publish-release-report.template.md` - publish result summary template.

### Implementation notes

- Skill naming:
  - `name` uses lowercase letters, digits, and hyphens.
  - Folder name must match `name`.

- Limits:
  - Keep `description` concise and trigger-oriented (prefer under 1024 chars).
  - Keep `SKILL.md` concise (prefer under 500 lines), move details to `references/`.

---

### Standardized Self-Test

- Probe token: `SKILL_PROBE_PUBLISH_RELEASE_WORKFLOW`
- Expected canary first line: `CANARY_PUBLISH_RELEASE_WORKFLOW_OK_20260210`
- Command:
  - `powershell -ExecutionPolicy Bypass -File .skills/run_skill_self_test.ps1 -ProjectRoot . -SkillName publish-release-workflow`
- Report file:
  - `temp/skill_probe_publish-release-workflow.md`
