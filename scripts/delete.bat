@echo off
setlocal EnableExtensions DisableDelayedExpansion

set "APM_DIR=%APPDATA%\apm"

echo [+] Uninstalling APM...

if exist "%APM_DIR%" (
    rd /S /Q "%APM_DIR%"
    if exist "%APM_DIR%" (
        echo [-] Failed to remove "%APM_DIR%".
        call :maybe_pause %*
        exit /b 1
    )
    echo [+] Removed "%APM_DIR%".
) else (
    echo [*] "%APM_DIR%" was not found.
)

call :remove_from_user_path "%APM_DIR%"
if errorlevel 1 (
    echo [!] Failed to update the user PATH automatically.
    echo [!] Remove "%APM_DIR%" from your PATH manually if needed.
) else (
    echo [+] PATH updated for the current user.
)

echo [+] APM uninstalled successfully.
call :maybe_pause %*
exit /b 0

:remove_from_user_path
setlocal EnableExtensions DisableDelayedExpansion
set "TARGET_DIR=%~1"
set "USER_PATH="

for /f "skip=2 tokens=2,*" %%A in ('reg query "HKCU\Environment" /v Path 2^>nul') do (
    if /I "%%A"=="REG_SZ" set "USER_PATH=%%B"
    if /I "%%A"=="REG_EXPAND_SZ" set "USER_PATH=%%B"
)

if not defined USER_PATH (
    endlocal & exit /b 0
)

setlocal EnableDelayedExpansion
set "PATH_CHECK=;!USER_PATH!;"
echo(!PATH_CHECK!| findstr /I /C:";%TARGET_DIR%;" >nul
if errorlevel 1 (
    endlocal
    endlocal & exit /b 0
)

set "NEW_PATH=;!USER_PATH!;"
:remove_again
set "UPDATED_PATH=!NEW_PATH:;%TARGET_DIR%;=;!"
if /I not "!UPDATED_PATH!"=="!NEW_PATH!" (
    set "NEW_PATH=!UPDATED_PATH!"
    goto :remove_again
)

if "!NEW_PATH:~0,1!"==";" set "NEW_PATH=!NEW_PATH:~1!"
if "!NEW_PATH:~-1!"==";" set "NEW_PATH=!NEW_PATH:~0,-1!"

if defined NEW_PATH (
    reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "!NEW_PATH!" /f >nul 2>&1
) else (
    reg delete "HKCU\Environment" /v Path /f >nul 2>&1
)

set "REG_ERROR=!ERRORLEVEL!"
endlocal
endlocal & exit /b %REG_ERROR%

:maybe_pause
if /I "%~1"=="--no-pause" exit /b 0
pause
exit /b 0
