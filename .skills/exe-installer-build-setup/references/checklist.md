# EXE and Installer Build Checklist

## Pre-build

- [ ] `VERSION.txt` exists and follows `x.y.z`.
- [ ] `build_app.bat`, `build_installer.bat`, and `setup.iss` exist.
- [ ] Inno Setup is available (if installer build is required).
- [ ] You accounted for `build_app.bat` auto patch bump behavior.

## During build

- [ ] `build_app.bat` completed successfully.
- [ ] `dist/DocCompareAI/DocCompareAI.exe` exists.
- [ ] `updater/Updater.exe` exists.
- [ ] `build_installer.bat` completed successfully.

## Post-build

- [ ] Installer output matches expected version filename.
- [ ] `installer/version.iss` matches `VERSION.txt`.
- [ ] Build summary has been recorded using the report template.
