# EXE and Installer Build Guideline

## Scope

Use this guideline for local build workflow:

- `build_app.bat`
- `build_installer.bat`
- `setup.iss`

## Standard build flow

1. Run preflight.
2. Build EXE with `build_app.bat`.
3. Build installer with `build_installer.bat`.
4. Validate artifacts and version consistency.

## Important version notes

1. `build_app.bat` auto-bumps patch version in `VERSION.txt`.
2. `build_installer.bat` reads `VERSION.txt` and writes `installer/version.iss`.
3. If you need to rebuild installer for the same version, avoid re-running `build_app.bat` unnecessarily.

## Required outputs

- `dist/DocCompareAI/DocCompareAI.exe`
- `updater/Updater.exe`
- `installer/DocCompareAI_Setup_v<version>.exe`

## Inno Setup rules

1. `build_installer.bat` requires `ISCC.exe`.
2. `ISCC.exe` lookup order:
   - `%INNO_SETUP%\\ISCC.exe`
   - `C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe`
   - `C:\\Program Files\\Inno Setup 6\\ISCC.exe`
3. If not found, fail fast with a clear error.

## Review focus

Prioritize:

1. Version sync across `VERSION.txt`, `installer/version.iss`, and installer filename.
2. Build script repeatability.
3. Error handling for missing dependencies or outputs.
