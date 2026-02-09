# Update Release Guideline (LAN)

## Scope

Use this guideline for desktop app updates distributed through a LAN share with pull-based update checks.

## Canonical layout

```text
<update-root>/
  LATEST.txt
  releases/
    <version>/
      version.json
      package.zip
      updater/Updater.exe
  changelog/
    <version>.txt
  installers/
    DocCompareAI_Setup_v<version>.exe
```

## Release protocol

1. Build app output (`dist/DocCompareAI`).
2. Package output to `package.zip`.
3. Generate `version.json` with `version`, `release_date`, `notes`, `package.path`, `package.sha256`, `package.size`, `app_exe`.
4. Upload release artifacts to `releases/<version>/`.
5. Upload changelog and installer (if required).
6. Update `LATEST.txt` last.

## Safety requirements

- Treat `VERSION.txt` as source of truth for app version.
- Never publish a release without a valid hash when `package.zip` is used.
- Never point `LATEST.txt` to a version before its artifact upload is complete.
- Keep updater separate from the main app process.

## Quick local test loop

1. Set `SSC_UPDATE_ROOT` to local project path.
2. Bump version in `VERSION.txt` and `dist/DocCompareAI/VERSION.txt`.
3. Run `publish_release.bat` with `SKIP_INSTALLER_CHECK=1`.
4. Launch an older installed app and click update.

## Review focus

Prioritize these checks during review:

1. Version consistency across source, dist, and manifest.
2. Hash calculation and manifest correctness.
3. Publish sequencing and rollback behavior.
4. Error handling for missing files or inaccessible share path.
