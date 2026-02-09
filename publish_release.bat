@echo off
setlocal EnableExtensions EnableDelayedExpansion

if "%PAUSE_ON_EXIT%"=="" set PAUSE_ON_EXIT=1
set LOG_FILE=publish_release.log
set EXITCODE=0
echo [%date% %time%] Publish started > "%LOG_FILE%"

set REMOTE_ROOT=\\10.1.3.2\KEIToolsData\SpreadSheetCompare
set DIST_DIR=dist\DocCompareAI
set CHANGELOG_DIR=changelog
set LOCAL_RELEASE_ROOT=releases
set INSTALLER_DIR=installer

if not exist "VERSION.txt" (
    call :fail "VERSION.txt not found. Please create it (e.g., 1.0.1)."
)
for /f "usebackq delims=" %%v in ("VERSION.txt") do set VERSION=%%v

if not exist "%DIST_DIR%\DocCompareAI.exe" (
    call :fail "Build output not found at %DIST_DIR%\\DocCompareAI.exe. Please run build_app.bat first."
)
if exist "%DIST_DIR%\VERSION.txt" (
    for /f "usebackq delims=" %%b in ("%DIST_DIR%\VERSION.txt") do set BUILD_VERSION=%%b
    if /I not "!BUILD_VERSION!"=="%VERSION%" (
        echo [WARNING] Build version mismatch. Build: !BUILD_VERSION!, Source: %VERSION%.
        echo [INFO] Updating dist version file to match source %VERSION%...
        echo %VERSION%> "%DIST_DIR%\VERSION.txt"
    )
) else (
    echo [INFO] dist\VERSION.txt not found. Creating it with version %VERSION%...
    echo %VERSION%> "%DIST_DIR%\VERSION.txt"
)

if not exist "%LOCAL_RELEASE_ROOT%" mkdir "%LOCAL_RELEASE_ROOT%"
set LOCAL_RELEASE_DIR=%LOCAL_RELEASE_ROOT%\%VERSION%
if not exist "%LOCAL_RELEASE_DIR%" mkdir "%LOCAL_RELEASE_DIR%"

set PACKAGE_PATH=%LOCAL_RELEASE_DIR%\package.zip

call :log "[1/5] Packaging release..."
powershell -NoProfile -Command "Compress-Archive -Path '%DIST_DIR%' -DestinationPath '%PACKAGE_PATH%' -Force"
if errorlevel 1 (
    call :fail "Failed to create package.zip"
)

call :log "[2/5] Calculating hash..."
for /f %%h in ('powershell -NoProfile -Command "(Get-FileHash -Algorithm SHA256 '%PACKAGE_PATH%').Hash.ToLower()"') do set HASH=%%h
for /f %%s in ('powershell -NoProfile -Command "(Get-Item '%PACKAGE_PATH%').Length"') do set SIZE=%%s
for /f %%d in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set RELDATE=%%d

set CHANGELOG_FILE=%CHANGELOG_DIR%\%VERSION%.txt

call :log "[3/5] Writing version.json..."
powershell -NoProfile -Command ^
  "$changelog='%CHANGELOG_FILE%';" ^
  "$notes='Release %VERSION%';" ^
  "if (Test-Path $changelog) { $lines = Get-Content $changelog; if ($lines.Count -gt 1) { $notes = ($lines[1..($lines.Count-1)] | Where-Object { $_ -match '\S' } | ForEach-Object { $_.TrimStart('-',' ') }) -join '; ' } };" ^
  "$obj = @{version='%VERSION%'; release_date='%RELDATE%'; notes=$notes; package=@{path='package.zip'; sha256='%HASH%'; size=%SIZE%}; app_exe='DocCompareAI.exe'};" ^
  "$json = $obj | ConvertTo-Json -Depth 4;" ^
  "[System.IO.File]::WriteAllText('%LOCAL_RELEASE_DIR%\version.json', $json, (New-Object System.Text.UTF8Encoding($false)))"

if exist "updater\Updater.exe" (
    if not exist "%LOCAL_RELEASE_DIR%\updater" mkdir "%LOCAL_RELEASE_DIR%\updater"
    copy /Y "updater\Updater.exe" "%LOCAL_RELEASE_DIR%\updater\" >nul
) else (
    call :log "WARNING: updater\\Updater.exe not found. Local release will not include updater."
)

call :log "[4/5] Checking installer..."
set EXPECTED_INSTALLER=%INSTALLER_DIR%\DocCompareAI_Setup_v%VERSION%.exe
if /I "%SKIP_INSTALLER_CHECK%"=="1" (
    call :log "Skipping installer check (SKIP_INSTALLER_CHECK=1)."
) else (
    if not exist "%EXPECTED_INSTALLER%" (
        set "FOUND_INSTALLER="
        for %%f in ("%INSTALLER_DIR%\DocCompareAI_Setup_v*.exe") do set "FOUND_INSTALLER=%%~f"
        if defined FOUND_INSTALLER (
            call :fail "Installer version mismatch. Found: !FOUND_INSTALLER!. Expected: %EXPECTED_INSTALLER%. Rebuild installer."
        ) else (
            call :fail "Installer not found. Expected: %EXPECTED_INSTALLER%. Build installer then re-run."
        )
    )
)

call :log "[5/5] Publishing to remote_root..."
if exist "%REMOTE_ROOT%" (
    if not exist "%REMOTE_ROOT%\releases" mkdir "%REMOTE_ROOT%\releases"
    if not exist "%REMOTE_ROOT%\releases\%VERSION%" mkdir "%REMOTE_ROOT%\releases\%VERSION%"
    if not exist "%REMOTE_ROOT%\changelog" mkdir "%REMOTE_ROOT%\changelog"
    if not exist "%REMOTE_ROOT%\installers" mkdir "%REMOTE_ROOT%\installers"

    copy /Y "%LOCAL_RELEASE_DIR%\package.zip" "%REMOTE_ROOT%\releases\%VERSION%\" >nul
    copy /Y "%LOCAL_RELEASE_DIR%\version.json" "%REMOTE_ROOT%\releases\%VERSION%\" >nul

    if exist "%CHANGELOG_FILE%" copy /Y "%CHANGELOG_FILE%" "%REMOTE_ROOT%\changelog\" >nul
    if /I not "%SKIP_INSTALLER_CHECK%"=="1" (
        copy /Y "%EXPECTED_INSTALLER%" "%REMOTE_ROOT%\installers\" >nul
    )

    if exist "updater\Updater.exe" (
        if not exist "%REMOTE_ROOT%\releases\%VERSION%\updater" mkdir "%REMOTE_ROOT%\releases\%VERSION%\updater"
        copy /Y "updater\Updater.exe" "%REMOTE_ROOT%\releases\%VERSION%\updater\" >nul
    )

    echo %VERSION%> "%REMOTE_ROOT%\LATEST.txt"
) else (
    call :log "WARNING: remote_root not found: %REMOTE_ROOT%. Skipping remote publish."
)

echo %VERSION%> "LATEST.txt"

call :log "Done. Published version %VERSION%."
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
