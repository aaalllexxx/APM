@echo off
python %APPDATA%/apm/apm.py %*
if exist "%TEMP%\apm_goto.tmp" (
    set /p APM_GOTO_PATH=<"%TEMP%\apm_goto.tmp"
    del "%TEMP%\apm_goto.tmp"
    cd /d "%APM_GOTO_PATH%"
)