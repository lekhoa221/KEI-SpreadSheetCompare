# Quick Update Test (No Rebuild Loop)

This guide lets you test the updater without rebuilding the EXE every time.

## One-time setup
1. Build once to create `dist\DocCompareAI` and `updater\Updater.exe`.
```
build_app.bat
```
2. Create a local test install folder and copy the build output.
```
mkdir C:\Apps\DocCompareAI_Test
xcopy /E /I /Y dist\DocCompareAI C:\Apps\DocCompareAI_Test
```
3. Point update checks to your local repo (so no server is required).
```
setx SSC_UPDATE_ROOT "C:\Users\Admin\Desktop\PersonalProject\SpreadSheetCompare"
```

## Fast test cycle (no rebuild)
1. Bump the version number in both places.
```
notepad VERSION.txt
notepad dist\DocCompareAI\VERSION.txt
```
2. Optional: add release notes for this version.
```
notepad changelog\<version>.txt
```
3. Publish the release locally (skip installer check to save time).
```
set SKIP_INSTALLER_CHECK=1
publish_release.bat
```
4. Open the old app and click Update.
```
C:\Apps\DocCompareAI_Test\DocCompareAI.exe
```

## Tips
1. To simulate another update, repeat the fast test cycle with a higher version.
2. To reset the “old app”, copy the previous build back into `C:\Apps\DocCompareAI_Test`.
3. If you want a full installer test, remove `SKIP_INSTALLER_CHECK=1` and build the installer normally.
