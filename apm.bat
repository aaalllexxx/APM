@echo off
setlocal

set "APM_HOME=%APPDATA%\apm"
set "APM_PYTHON=%APM_HOME%\venv\Scripts\python.exe"

if exist "%APM_PYTHON%" (
    "%APM_PYTHON%" "%APM_HOME%\apm.py" %*
) else (
    python "%APM_HOME%\apm.py" %*
)

if not exist "%TEMP%\apm_goto.tmp" goto :eof

set /p APM_GOTO_PATH=<"%TEMP%\apm_goto.tmp"
del "%TEMP%\apm_goto.tmp"
cd /d "%APM_GOTO_PATH%"
set "APM_GOTO_PATH="
