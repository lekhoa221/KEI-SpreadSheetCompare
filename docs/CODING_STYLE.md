# Coding Style & Philosophy

## 1. Core Philosophy: "Premium Utility"
- We do not build "scripts"; we build **Products**.
- Even internal tools must look and feel professional.
- **Visuals Matter**: A slightly slower app that looks beautiful is often trusted more than a fast, ugly one.
- **Fail Gracefully**: If a complex feature (like Borders) looks bad, remove it rather than ship it broken. Keep it clean.

## 2. Python / PyQt Patterns
- **Modularization**: One file for one major component (`main_window.py`, `result_view.py`). Logic goes in `core/`.
- **Threading**: heavy logic (File I/O, Analysis) **ALWAYS** goes to a `QThread` (Worker). Freezing the GUI is unacceptable.
- **Signals/Slots**: Use Qt's signal system for decoupling components.
- **Type Hinting**: Use Python type hints where helpful for readability (`df: pd.DataFrame`).

## 3. UI/UX Standards
- **Theme**: Light Mode default (Professional/Office suite standard).
- **Colors**:
    - Primary Action: Excel Green (`#107c41`).
    - Secondary/Destructive: Red (`#c5221f`).
    - Selection: High contrast Blue (`#2563eb`).
    - Backgrounds: Off-white (`#f3f4f6`) to reduce eye strain compared to pure white.
- **Feedback**: Buttons must change state (disabled/processing) when clicked. Tooltips providing context are mandatory for complex cells.

## 4. Git / Versioning
- **Checkpoints**: Commit/Save working states before major refactors.
- **Feature Flags**: Toggle features (like Word/PPT support) via UI visibility rather than commenting out code if possible.
