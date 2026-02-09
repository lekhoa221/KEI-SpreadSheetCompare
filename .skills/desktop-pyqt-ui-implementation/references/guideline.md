# Desktop PyQt UI Guideline

## Scope

Use this guideline for desktop UI work in:

- `desktop_app.py`
- `ui/`
- closely related core helpers consumed by desktop UI (`core/config.py`, `core/update_manager.py`, `core/feedback_manager.py`)

## Architecture baseline

1. Startup and splash flow is handled in `desktop_app.py`.
2. Main window orchestration is handled in `ui/main_window.py`.
3. Result grid interaction is handled in `ui/excel/result_view.py`.
4. File picker and drag-drop is handled in `ui/file_drop.py`.

## Implementation protocol

1. Understand affected UI flow before editing:
   - startup and theme setup
   - file loading and validation
   - background comparison thread
   - result visualization and interaction
2. Keep changes localized to the smallest set of widgets and handlers.
3. Preserve signal and slot compatibility unless contract changes are required.
4. Keep heavy computation off the UI thread.

## PyInstaller and path rules

1. Preserve runtime path handling for both source and frozen mode.
2. Do not break `sys._MEIPASS` asset resolution behavior.
3. Keep icon and asset loading resilient to missing files.

## UI and UX rules

1. Maintain consistent style via object names and central stylesheet.
2. Keep loading and error feedback visible and actionable.
3. Preserve keyboard and selection behavior in result grids.
4. Ensure layout remains usable at minimum window size.

## Review focus

Prioritize these checks:

1. Thread safety and UI responsiveness.
2. Selection and scroll synchronization behavior.
3. State transitions between dashboard and result views.
4. Regression risk in update prompt and feedback actions.
