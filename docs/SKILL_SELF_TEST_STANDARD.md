# Skill Self-Test Standard

This document defines a single standardized self-test process for all local project skills.

## 1. Single command entrypoint

Use one command for every skill:

```powershell
powershell -ExecutionPolicy Bypass -File .skills/run_skill_self_test.ps1 -ProjectRoot . -SkillName <skill-name>
```

Use strict mode when needed:

```powershell
powershell -ExecutionPolicy Bypass -File .skills/run_skill_self_test.ps1 -ProjectRoot . -SkillName <skill-name> -Strict
```

## 2. Supported skills

| Skill name | Probe token | Canary first line | Report path |
| --- | --- | --- | --- |
| `update-release-workflow` | `SKILL_PROBE_UPDATE_RELEASE_WORKFLOW` | `CANARY_UPDATE_RELEASE_WORKFLOW_OK_20260210` | `temp/skill_probe_update-release-workflow.md` |
| `frontend-ui-implementation` | `SKILL_PROBE_FRONTEND_UI_IMPLEMENTATION` | `CANARY_FRONTEND_UI_IMPLEMENTATION_OK_20260210` | `temp/skill_probe_frontend-ui-implementation.md` |
| `backend-api-implementation` | `SKILL_PROBE_BACKEND_API_IMPLEMENTATION` | `CANARY_BACKEND_API_IMPLEMENTATION_OK_20260210` | `temp/skill_probe_backend-api-implementation.md` |
| `desktop-pyqt-ui-implementation` | `SKILL_PROBE_DESKTOP_PYQT_UI_IMPLEMENTATION` | `CANARY_DESKTOP_PYQT_UI_IMPLEMENTATION_OK_20260210` | `temp/skill_probe_desktop-pyqt-ui-implementation.md` |
| `checklist-backlog-governor` | `SKILL_PROBE_CHECKLIST_BACKLOG_GOVERNOR` | `CANARY_CHECKLIST_BACKLOG_GOVERNOR_OK_20260210` | `temp/skill_probe_checklist-backlog-governor.md` |
| `exe-installer-build-setup` | `SKILL_PROBE_EXE_INSTALLER_BUILD_SETUP` | `CANARY_EXE_INSTALLER_BUILD_SETUP_OK_20260210` | `temp/skill_probe_exe-installer-build-setup.md` |
| `publish-release-workflow` | `SKILL_PROBE_PUBLISH_RELEASE_WORKFLOW` | `CANARY_PUBLISH_RELEASE_WORKFLOW_OK_20260210` | `temp/skill_probe_publish-release-workflow.md` |

## 3. Prompt template for interactive AI probe

Use this in a fresh chat:

```text
Use $<skill-name>.
<probe-token>
Run only the standardized self-test protocol and report the generated report file path.
```

Example:

```text
Use $exe-installer-build-setup.
SKILL_PROBE_EXE_INSTALLER_BUILD_SETUP
Run only the standardized self-test protocol and report the generated report file path.
```

## 4. PASS criteria

1. First output line exactly matches that skill's canary line.
2. The report file is generated in `temp/`.
3. The report `Final status` is `PASS`.
