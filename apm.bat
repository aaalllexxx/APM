@echo off
setlocal EnableExtensions DisableDelayedExpansion

set "APM_DIR=%APPDATA%\apm"
set "VENV_PYTHON=%APM_DIR%\venv\Scripts\python.exe"
set "RUNNER_PYTHON="

if exist "%VENV_PYTHON%" (
    set "RUNNER_PYTHON=%VENV_PYTHON%"
) else (
    set "RUNNER_PYTHON=python"
)

"%RUNNER_PYTHON%" "%APM_DIR%\apm.py" %*
set "APM_EXIT_CODE=%ERRORLEVEL%"

if not exist "%TEMP%\apm_goto.tmp" (
    exit /b %APM_EXIT_CODE%
)

set /p APM_GOTO_PATH=<"%TEMP%\apm_goto.tmp"
del "%TEMP%\apm_goto.tmp" >nul 2>&1
if defined APM_GOTO_PATH (
    cd /d "%APM_GOTO_PATH%"
)

set "APM_GOTO_PATH="
exit /b %APM_EXIT_CODE%
