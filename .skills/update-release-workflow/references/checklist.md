# Update Release Checklist

## Pre-release

- [ ] `VERSION.txt` exists and matches expected semantic version (`x.y.z`).
- [ ] `dist/DocCompareAI/DocCompareAI.exe` exists.
- [ ] `dist/DocCompareAI/VERSION.txt` matches `VERSION.txt`.
- [ ] `publish_release.bat` exists and uses current release root rules.
- [ ] Changelog for the target version exists (recommended).
- [ ] Installer exists when publishing official release (`installer/DocCompareAI_Setup_v<version>.exe`).

## Release execution

- [ ] Run preflight script with correct project root.
- [ ] Build/publish scripts finish without error.
- [ ] `version.json` contains correct version, date, notes, package metadata.
- [ ] `package.zip` hash matches `version.json.package.sha256`.
- [ ] Artifacts are uploaded to `releases/<version>/`.
- [ ] `LATEST.txt` is updated only after all artifacts are in place.

## Post-release validation

- [ ] Client detects new version via `LATEST.txt`.
- [ ] Client reads `version.json` successfully.
- [ ] Updater can apply update and relaunch app.
- [ ] Updated app launches and basic workflows run normally.

## Rollback

- [ ] Rollback target version is known and available.
- [ ] `LATEST.txt` can be reset quickly to previous stable version.
- [ ] Team has a short incident note with root cause and fix plan.
