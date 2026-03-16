@echo off
setlocal enabledelayedexpansion

:: AEngine Unified Installer for Windows
:: This script sets up APM, Security module, and all project dependencies.

set "PROJECT_ROOT=%~dp0"
set "APM_DIR=%APPDATA%\apm"

echo ==========================================
echo     AEngine Zero-Configuration Setup
echo ==========================================

:: Create config directory
if not exist "%APM_DIR%" mkdir "%APM_DIR%"
if not exist "%APM_DIR%\modules" mkdir "%APM_DIR%\modules"

:: Create virtual environment
echo [+] Creating virtual environment in %APM_DIR%\venv...
python -m venv "%APM_DIR%\venv"
if errorlevel 1 (
    echo [-] Failed to create virtual environment. Ensure Python is in PATH.
    pause
    exit /b 1
)

:: Update pip and install requirements
echo [+] Updating pip...
"%APM_DIR%\venv\Scripts\python.exe" -m pip install --upgrade pip

echo [+] Installing project dependencies...
if exist "%PROJECT_ROOT%\requirements.txt" (
    "%APM_DIR%\venv\Scripts\python.exe" -m pip install -r "%PROJECT_ROOT%\requirements.txt"
) else (
    echo [!] requirements.txt not found.
)

:: Copy APM files
echo [+] Synchronizing APM modules...
xcopy /E /Y /Q "%PROJECT_ROOT%APM\*" "%APM_DIR%\"

:: Add to user PATH if not already there
echo [+] Registering 'apm' command for current user...
setx PATH "%PATH%;%APM_DIR%" >nul 2>&1

echo.
echo [+] Setup complete! AEngine is ready to use.
echo [+] Please restart your terminal/IDE to use 'apm' command.
echo ==========================================
pause
