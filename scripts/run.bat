@echo off
:: ============================================================
:: Smart AI Growth Hub — Content Pipeline Runner
:: Run this file from the project root or double-click it.
:: ============================================================

setlocal EnableDelayedExpansion

:: --- Resolve the project root (one level up from this script)
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."

:: --- Move to project root so relative paths work correctly
cd /d "%PROJECT_ROOT%"

echo.
echo ============================================================
echo   Smart AI Growth Hub — AI Content Pipeline
echo ============================================================
echo   Project root : %CD%
echo   Script       : scripts\generate_content.py
echo ============================================================
echo.

:: --- Find Python (try 'python', then the 'py' launcher)
set "PY_CMD="
python --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=python"
) else (
    py --version >nul 2>&1
    if not errorlevel 1 (
        set "PY_CMD=py"
    )
)

if not defined PY_CMD (
    echo [ERROR] Python is not installed or not on your PATH.
    echo         Download Python 3 from https://www.python.org/downloads/
    echo         Make sure to check "Add Python to PATH" during install.
    echo         Then close and reopen this window and try again.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('!PY_CMD! --version 2^>^&1') do set PY_VER=%%i
echo   Using: %PY_VER% ^(!PY_CMD!^)
echo.

:: --- Run the generator
echo   Starting content generation...
echo   (This may take a moment for all keywords)
echo.

!PY_CMD! scripts\generate_content.py

:: --- Check exit code
if errorlevel 1 (
    echo.
    echo [ERROR] The script exited with an error. Check the log file in:
    echo         outputs\logs\
    echo.
) else (
    echo.
    echo ============================================================
    echo   Generation complete!
    echo ============================================================
    echo.
    echo   Blog HTML files  : outputs\blog_html\
    echo   Pinterest CSVs   : outputs\pinterest_csv\
    echo   Updated tracker  : keywords\keywords.csv
    echo   Log file         : outputs\logs\
    echo.
    echo   Next step: Open keywords\keywords.csv to review results,
    echo   then upload outputs\ to Google Drive for Make.com publishing.
    echo ============================================================
)

echo.
pause
