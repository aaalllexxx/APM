@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "APM_ROOT=%%~dpfI"
set "APM_DIR=%APPDATA%\apm"
set "VENV_PYTHON=%APM_DIR%\venv\Scripts\python.exe"

echo ==========================================
echo     AEngine Zero-Configuration Setup
echo ==========================================

if not exist "%APM_DIR%" mkdir "%APM_DIR%"
if not exist "%APM_DIR%\modules" mkdir "%APM_DIR%\modules"

echo [+] Creating virtual environment in %APM_DIR%\venv...
python -m venv "%APM_DIR%\venv"
if errorlevel 1 (
    echo [-] Failed to create virtual environment. Ensure Python is in PATH.
    pause
    exit /b 1
)

echo [+] Updating pip...
"%VENV_PYTHON%" -m pip install --upgrade pip

echo [+] Installing core APM dependencies...
"%VENV_PYTHON%" -m pip install colorama==0.4.6 cursor==1.3.5 readchar markdown-it-py==3.0.0 mdurl==0.1.2 Pygments==2.17.2 rich==13.7.1 flask GitPython
if errorlevel 1 (
    echo [-] Failed to install core dependencies.
    pause
    exit /b 1
)

echo [+] Installing optional desktop dependency pywebview...
"%VENV_PYTHON%" -m pip install pywebview
if errorlevel 1 (
    echo [!] pywebview was not installed. APM will work, but desktop/webview mode may require manual installation later.
)

echo [+] Synchronizing APM modules...
xcopy /E /Y /Q "%APM_ROOT%\*" "%APM_DIR%\"

echo [+] Registering 'apm' command for current user...
setx PATH "%PATH%;%APM_DIR%" >nul 2>&1

echo.
echo [+] Setup complete! AEngine is ready to use.
echo [+] APM will use its own virtual environment: %VENV_PYTHON%
echo [+] Please restart your terminal/IDE to use 'apm' command.
echo ==========================================
pause
