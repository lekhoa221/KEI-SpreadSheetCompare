@echo off
setlocal EnableExtensions

if not exist "desktop_app.py" (
    echo desktop_app.py not found in current folder.
    exit /b 1
)

set "PY_EXE="
if exist "venv\Scripts\python.exe" set "PY_EXE=venv\Scripts\python.exe"
if "%PY_EXE%"=="" set "PY_EXE=python"
if "%SSC_DEFAULT_TIMEZONE%"=="" set "SSC_DEFAULT_TIMEZONE=Asia/Bangkok"

echo Running: %PY_EXE% desktop_app.py
call %PY_EXE% desktop_app.py
exit /b %errorlevel%
