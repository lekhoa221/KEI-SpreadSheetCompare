# Publish Release Checklist

## Pre-publish

- [ ] `VERSION.txt` exists and matches expected release version.
- [ ] `dist/DocCompareAI/DocCompareAI.exe` exists.
- [ ] `publish_release.bat` exists and is the intended publish entrypoint.
- [ ] Installer output exists for strict publish mode.
- [ ] Optional changelog file exists for the target version.

## During publish

- [ ] Package zip is created successfully.
- [ ] SHA256 hash and file size are computed.
- [ ] `version.json` is generated with correct fields.
- [ ] Local release folder contains package and manifest.
- [ ] Remote copy completed without file-not-found failures.

## Post-publish

- [ ] Remote release folder contains expected artifacts.
- [ ] `LATEST.txt` points to the intended version.
- [ ] Local `LATEST.txt` was updated consistently.
- [ ] Publish result summary has been recorded.
