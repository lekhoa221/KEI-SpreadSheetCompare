@echo off
setlocal EnableExtensions EnableDelayedExpansion
set PAUSE_ON_EXIT=1
set LOG_FILE=build_app.log
set EXITCODE=0
echo [%date% %time%] Build started > "%LOG_FILE%"

echo ==========================================
echo      SpreadSheetCompare Build Script
echo ==========================================

echo [0/6] Checking for Virtual Environment...
if exist "venv\Scripts\activate.bat" (
    echo    Found venv, activating...
    call venv\Scripts\activate.bat
) else (
    echo    No venv found in project root. Using system Python.
)

echo [1/6] Auto Bump ^& Sync Version...
if not exist "VERSION.txt" (
    echo 1.0.0> VERSION.txt
)
for /f "usebackq delims=" %%v in ("VERSION.txt") do set OLD_VERSION=%%v

rem Bump version (Patch level)
for /f %%n in ('powershell -NoProfile -Command "$v='%OLD_VERSION%'; $p=$v.Split('.'); $p[-1]=[int]$p[-1]+1; $p -join '.'"') do set APP_VERSION=%%n

echo %APP_VERSION%> VERSION.txt
echo    Bumped version: %OLD_VERSION% -^> %APP_VERSION%
if not exist "installer" mkdir "installer"
echo #define MyAppVersion "%APP_VERSION%"> "installer\version.iss"
powershell -NoProfile -Command ^
  "$v='%APP_VERSION%';" ^
  "$p='core/version.py';" ^
  "$content = Get-Content $p;" ^
  "$content = $content -replace 'DEFAULT_VERSION = \".*\"', ('DEFAULT_VERSION = \"' + $v + '\"');" ^
  "$content | Set-Content -Path $p -Encoding UTF8"

echo [2/6] Installing Dependencies...
echo    Installing core libraries...
pip install PyQt6 pandas openpyxl pillow pyinstaller pytz tzdata --quiet
if errorlevel 1 call :fail "pip install core libraries failed"
pip install pyqtdarktheme --quiet
if errorlevel 1 echo    Warning: pyqtdarktheme installation failed, but checking import...
python -c "import qdarktheme" >nul 2>&1 || call :fail "qdarktheme module is required for build. Please install it and retry."
python -c "import pytz" >nul 2>&1 || call :fail "pytz is required for build. Please install it and retry."

echo [3/6] Generating Icon...
if not exist "app_icon.ico" (
    python create_icon.py
    if errorlevel 1 call :fail "Failed to generate app_icon.ico"
)

echo [4/6] Building Exe (clean build)...
rem Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

rem Run PyInstaller
rem --hidden-import might be needed for pandas/openpyxl engine dependencies sometimes
rem --exclude-module keeps heavy AI/OCR libs out of the package when not used
if exist "DocCompareAI.spec" (
    pyinstaller --noconfirm DocCompareAI.spec
) else (
    pyinstaller --noconsole --name "DocCompareAI" --icon "app_icon.ico" --add-data "ui/assets;ui/assets" --hidden-import "pandas" --hidden-import "openpyxl" --hidden-import "qdarktheme" --hidden-import "PyQt6.QtSvg" --hidden-import "PyQt6.QtWidgets" --hidden-import "PyQt6.QtCore" --hidden-import "PyQt6.QtGui" ^
        --exclude-module "torch" --exclude-module "torchvision" --exclude-module "torchaudio" ^
        --exclude-module "paddle" --exclude-module "paddleocr" --exclude-module "easyocr" ^
        --exclude-module "cv2" --exclude-module "opencv" ^
        --exclude-module "transformers" --exclude-module "onnxruntime" --exclude-module "bitsandbytes" ^
        --exclude-module "scipy" --exclude-module "sklearn" --exclude-module "sentencepiece" ^
        desktop_app.py
)
if errorlevel 1 call :fail "PyInstaller build failed"

echo.
echo ==========================================
if exist "dist\DocCompareAI\DocCompareAI.exe" (
    echo BUILD SUCCESSFUL!
    echo Application is located in: dist\DocCompareAI
    copy /Y "VERSION.txt" "dist\DocCompareAI\VERSION.txt" >nul
) else (
    call :fail "Build output not found. Check errors above."
)
echo ==========================================

echo [5/6] Building Installer (Inno Setup)...
set ISCC_PATH=
if exist "%INNO_SETUP%\ISCC.exe" set ISCC_PATH=%INNO_SETUP%\ISCC.exe
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" set ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe

if not "%ISCC_PATH%"=="" (
    "%ISCC_PATH%" "setup.iss"
    if errorlevel 1 (
        call :log "Installer build failed. Please check Inno Setup output."
    ) else (
        call :log "Installer build successful."
    )
) else (
    call :log "Inno Setup not found. Set INNO_SETUP to the install folder or install Inno Setup 6."
)

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
