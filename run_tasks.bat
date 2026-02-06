@echo off
setlocal EnableExtensions EnableDelayedExpansion
set "PAUSE_ON_EXIT=0"

:menu
echo.
echo ==========================================
echo          Build / Publish Menu
echo ==========================================
echo 1. Build EXE
echo 2. Build Installer
echo 3. Publish
echo 4. Set Version
echo 5. Open Server Folder
echo 6. Run App (desktop_app.py)
echo X. Exit
echo ==========================================
set /p choice="Choose (e.g. 1, 23, 13, 123, 4, 45, 6, x): "

set choice=!choice: =!
set choice=!choice:,=!

if /i "!choice!"=="x" goto :end
if "!choice!"=="" goto :menu

set do1=0
set do2=0
set do3=0
set do4=0
set do5=0
set do6=0

echo !choice! | findstr /c:"1" >nul && set do1=1
echo !choice! | findstr /c:"2" >nul && set do2=1
echo !choice! | findstr /c:"3" >nul && set do3=1
echo !choice! | findstr /c:"4" >nul && set do4=1
echo !choice! | findstr /c:"5" >nul && set do5=1
echo !choice! | findstr /c:"6" >nul && set do6=1

if "!do1!!do2!!do3!!do4!!do5!!do6!"=="000000" (
    echo Invalid choice. Try again.
    goto :menu
)

if "!do4!"=="1" (
    call :set_version
    if errorlevel 1 goto :menu
)
if "!do1!"=="1" (
    call :run_task "Build EXE" build_app.bat
    if errorlevel 1 goto :menu
)
if "!do2!"=="1" (
    call :run_task "Build Installer" build_installer.bat
    if errorlevel 1 goto :menu
)
if "!do3!"=="1" (
    if not "!do2!"=="1" (
        set "SKIP_INSTALLER_CHECK=1"
    ) else (
        set "SKIP_INSTALLER_CHECK="
    )
    call :run_task "Publish" publish_release.bat
    if errorlevel 1 goto :menu
    set "SKIP_INSTALLER_CHECK="
)
if "!do5!"=="1" (
    call :open_server
)
if "!do6!"=="1" (
    call run_desktop.bat
)

goto :menu

:run_task
set "taskName=%~1"
set "taskCmd=%~2"
echo.
echo ---------- %taskName% ----------
call %taskCmd%
if errorlevel 1 (
    echo [FAILED] %taskName%
    exit /b 1
)
echo [DONE] %taskName%
exit /b 0

:set_version
set "NEW_VERSION="
set /p NEW_VERSION="Enter version (e.g. v1.1.0 or 2.1.0): "
set "NEW_VERSION=!NEW_VERSION: =!"
if "!NEW_VERSION!"=="" (
    echo Empty version. Cancelled.
    exit /b 1
)
for /f "usebackq delims=" %%v in (`powershell -NoProfile -Command "$v='!NEW_VERSION!'.Trim(); if ($v -match '^[vV]') { $v = $v.Substring(1) }; if ($v -notmatch '^[0-9]+(\\.[0-9]+){2,3}$') { exit 1 }; $v"`) do set "NEW_VERSION=%%v"
if "!NEW_VERSION!"=="" (
    echo Invalid version format. Use 1.2.3 (optionally with leading v).
    exit /b 1
)
echo !NEW_VERSION!> VERSION.txt
if not exist "installer" mkdir "installer"
echo #define MyAppVersion "!NEW_VERSION!"> "installer\version.iss"
if exist "dist\\DocCompareAI\\VERSION.txt" (
    echo !NEW_VERSION!> "dist\\DocCompareAI\\VERSION.txt"
)
powershell -NoProfile -Command ^
  "$v='!NEW_VERSION!';" ^
  "$p='core/version.py';" ^
  "$content = Get-Content $p;" ^
  "$content = $content -replace 'DEFAULT_VERSION = \".*\"', ('DEFAULT_VERSION = \"' + $v + '\"');" ^
  "$content | Set-Content -Path $p -Encoding UTF8"
echo Version set to !NEW_VERSION!.
exit /b 0

:open_server
set "SERVER_ROOT=\\10.1.3.2\KEIToolsData\SpreadSheetCompare"
if exist "%SERVER_ROOT%" (
    start "" "%SERVER_ROOT%"
    exit /b 0
)
echo Server path not found: %SERVER_ROOT%
exit /b 1

:end
endlocal
