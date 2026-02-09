# Desktop PyQt UI Checklist

## Pre-implementation

- [ ] Confirm scope: startup, dashboard, compare flow, result view, or utility dialog.
- [ ] Identify impacted files in `desktop_app.py` and `ui/`.
- [ ] Run desktop preflight script.

## Implementation

- [ ] Keep long-running operations out of main UI thread.
- [ ] Keep signal and slot connections clear and deterministic.
- [ ] Keep style updates consistent with existing object names.
- [ ] Keep file path logic compatible with source and frozen modes.
- [ ] Avoid touching unrelated frontend/backend code.

## Verification

- [ ] Run compile check for desktop UI files.
- [ ] Run app via `run_desktop.bat`.
- [ ] Verify upload and compare flow still works.
- [ ] Verify result view interactions (selection, scroll sync, zoom, filter).
- [ ] Verify key error paths show user-friendly messages.

## Handoff

- [ ] Document behavior changes and assumptions.
- [ ] List changed files and why.
- [ ] Record follow-up tasks if debt remains.
