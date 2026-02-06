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
echo X. Exit
echo ==========================================
set /p choice="Choose (e.g. 1, 23, 13, 123, x): "

set choice=!choice: =!
set choice=!choice:,=!

if /i "!choice!"=="x" goto :end
if "!choice!"=="" goto :menu

set do1=0
set do2=0
set do3=0

echo !choice! | findstr /c:"1" >nul && set do1=1
echo !choice! | findstr /c:"2" >nul && set do2=1
echo !choice! | findstr /c:"3" >nul && set do3=1

if "!do1!!do2!!do3!"=="000" (
    echo Invalid choice. Try again.
    goto :menu
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

:end
endlocal
