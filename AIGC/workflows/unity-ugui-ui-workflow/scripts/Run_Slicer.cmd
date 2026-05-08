@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo  Unity UI Auto Slicer v2 - no cv2 / OpenCV
echo ============================================================
echo.

set "PY_CMD="
py -3 --version >nul 2>&1
if not errorlevel 1 set "PY_CMD=py -3"

if "%PY_CMD%"=="" (
    python --version >nul 2>&1
    if not errorlevel 1 set "PY_CMD=python"
)

if "%PY_CMD%"=="" (
    echo Python 3 was not found.
    echo Download Python: https://www.python.org/downloads/
    echo Make sure to check: Add python.exe to PATH
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating local Python environment...
    %PY_CMD% -m venv .venv
    if errorlevel 1 (
        echo Failed to create the local Python environment.
        pause
        exit /b 1
    )
)

set "PY=.venv\Scripts\python.exe"

echo Installing/updating Pillow...
"%PY%" -m pip install --upgrade pip >nul 2>&1
"%PY%" -m pip install --upgrade pillow
if errorlevel 1 (
    echo.
    echo Failed to install Pillow.
    echo Try manually in this folder:
    echo .venv\Scripts\python.exe -m pip install pillow
    pause
    exit /b 1
)

echo.
"%PY%" "%~dp0unity_ui_auto_slicer.py"

echo.
pause
