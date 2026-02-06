@echo off
setlocal EnableExtensions EnableDelayedExpansion
if "%PAUSE_ON_EXIT%"=="" set PAUSE_ON_EXIT=1
set LOG_FILE=build_installer.log
set EXITCODE=0
echo [%date% %time%] Installer build started > "%LOG_FILE%"

echo ==========================================
echo     SpreadSheetCompare Installer Script
echo ==========================================

echo [0/2] Checking version and build output...
if not exist "VERSION.txt" (
    call :fail "VERSION.txt not found. Please create it (e.g., 1.0.1)."
)
for /f "usebackq delims=" %%v in ("VERSION.txt") do set APP_VERSION=%%v
if not exist "installer" mkdir "installer"
echo #define MyAppVersion "%APP_VERSION%"> "installer\version.iss"

if not exist "dist\DocCompareAI\DocCompareAI.exe" (
    call :fail "Build output not found at dist\\DocCompareAI\\DocCompareAI.exe. Run build_app.bat first."
)

echo [1/2] Building Installer (Inno Setup)...
set ISCC_PATH=
if exist "%INNO_SETUP%\ISCC.exe" set ISCC_PATH=%INNO_SETUP%\ISCC.exe
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" set ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe

if not "%ISCC_PATH%"=="" (
    "%ISCC_PATH%" "setup.iss"
    if errorlevel 1 (
        call :fail "Installer build failed. Please check Inno Setup output."
    ) else (
        call :log "Installer build successful."
    )
) else (
    call :fail "Inno Setup not found. Set INNO_SETUP to the install folder or install Inno Setup 6."
)

echo [2/2] Done.
echo ==========================================
goto :end

:log
echo %~1
echo [%date% %time%] %~1>> "%LOG_FILE%"
exit /b 0

:fail
set EXITCODE=1
call :log "ERROR: %~1"
goto :end

:end
if "%PAUSE_ON_EXIT%"=="1" pause
endlocal & exit /b %EXITCODE%
