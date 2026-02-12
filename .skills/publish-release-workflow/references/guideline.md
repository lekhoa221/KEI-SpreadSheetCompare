# Publish Release Guideline

## Scope

Use this guideline for release publishing tasks involving:

- `publish_release.bat`
- local release artifacts in `releases/`
- remote publish target and `LATEST.txt` switching

## Standard publish flow

1. Validate prerequisites (version, build outputs, installer as needed).
2. Package dist output into `package.zip`.
3. Generate hash and size.
4. Write `version.json`.
5. Copy artifacts to local release folder.
6. Publish to remote path.
7. Update `LATEST.txt` last.

## Artifact expectations

Required:

- `releases/<version>/package.zip`
- `releases/<version>/version.json`

Optional but recommended:

- `releases/<version>/updater/Updater.exe`
- `changelog/<version>.txt`
- `installer/DocCompareAI_Setup_v<version>.exe` for full release mode

## Safety rules

1. Never switch `LATEST.txt` before artifact copy is complete.
2. Keep `version.json` aligned with package hash and size.
3. Keep version source anchored to `VERSION.txt`.
4. Fail fast for missing required artifacts.

## Review focus

Prioritize:

1. Publish ordering and atomicity.
2. Version consistency across source, dist, and manifest.
3. Installer expectation logic (`SKIP_INSTALLER_CHECK` vs strict mode).
4. Remote copy behavior and fallback warnings.
