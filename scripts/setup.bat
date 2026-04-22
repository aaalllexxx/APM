@echo off
setlocal EnableExtensions DisableDelayedExpansion

rem AEngine Unified Installer for Windows
rem Installs APM into the current user's profile without requiring admin rights.

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "PROJECT_ROOT=%%~fI"
set "APM_DIR=%APPDATA%\apm"
set "VENV_DIR=%APM_DIR%\venv"
set "PYTHON_EXE="
set "PYTHON_VERSION="
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"

echo ==========================================
echo     AEngine Zero-Configuration Setup
echo ==========================================

call :find_python
if not defined PYTHON_EXE (
    echo [-] Python 3 was not found.
    echo [!] Install Python 3 and make sure "py" or "python" is available in PATH.
    call :maybe_pause %*
    exit /b 1
)

call :read_python_version "%PYTHON_EXE%" PYTHON_VERSION
if not defined PYTHON_VERSION (
    echo [-] Failed to determine the Python version for "%PYTHON_EXE%".
    call :maybe_pause %*
    exit /b 1
)

call :is_supported_python "%PYTHON_VERSION%"
if errorlevel 1 (
    echo [-] Unsupported Python version detected: %PYTHON_VERSION%
    echo [!] Install Python 3.10, 3.11, 3.12, or 3.13 and run setup again.
    call :maybe_pause %*
    exit /b 1
)

echo [+] Using Python %PYTHON_VERSION%: %PYTHON_EXE%

if not exist "%APM_DIR%" mkdir "%APM_DIR%"
if errorlevel 1 (
    echo [-] Failed to create "%APM_DIR%".
    call :maybe_pause %*
    exit /b 1
)

if not exist "%APM_DIR%\modules" mkdir "%APM_DIR%\modules"

if exist "%VENV_PYTHON%" (
    set "VENV_VERSION="
    call :read_python_version "%VENV_PYTHON%" VENV_VERSION
    if /I "%VENV_VERSION%"=="%PYTHON_VERSION%" (
        echo [+] Reusing existing virtual environment in %VENV_DIR%.
    ) else (
        echo [!] Existing virtual environment uses Python %VENV_VERSION%. Recreating it for Python %PYTHON_VERSION%...
        rmdir /S /Q "%VENV_DIR%" >nul 2>&1
        if exist "%VENV_DIR%" (
            echo [-] Failed to remove the old virtual environment at "%VENV_DIR%".
            call :maybe_pause %*
            exit /b 1
        )
        goto :create_venv
    )
) else (
    if exist "%VENV_DIR%" (
        echo [!] Incomplete virtual environment detected. Recreating %VENV_DIR%...
        rmdir /S /Q "%VENV_DIR%" >nul 2>&1
        if exist "%VENV_DIR%" (
            echo [-] Failed to remove the incomplete virtual environment at "%VENV_DIR%".
            call :maybe_pause %*
            exit /b 1
        )
    )
    goto :create_venv
)
goto :venv_ready

:create_venv
echo [+] Creating virtual environment in %VENV_DIR%...
"%PYTHON_EXE%" -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo [-] Failed to create virtual environment.
    call :maybe_pause %*
    exit /b 1
)

:venv_ready

if not exist "%VENV_PYTHON%" (
    echo [-] Virtual environment was created incorrectly: "%VENV_PYTHON%" was not found.
    call :maybe_pause %*
    exit /b 1
)

echo [+] Updating pip...
"%VENV_PYTHON%" -m pip install --upgrade pip
if errorlevel 1 (
    echo [!] Failed to upgrade pip. Continuing with the bundled version.
)

echo [+] Installing project dependencies...
if exist "%PROJECT_ROOT%\requirements.txt" (
    "%VENV_PYTHON%" -m pip install -r "%PROJECT_ROOT%\requirements.txt"
    if errorlevel 1 (
        echo [-] Failed to install dependencies from requirements.txt.
        call :maybe_pause %*
        exit /b 1
    )
) else (
    echo [!] requirements.txt not found at "%PROJECT_ROOT%\requirements.txt".
)

echo [+] Synchronizing APM files...
xcopy "%PROJECT_ROOT%\*" "%APM_DIR%\" /E /I /Y /Q /EXCLUDE:"%SCRIPT_DIR%xcopy_exclude.txt" >nul
if errorlevel 2 (
    echo [-] Failed to copy project files into "%APM_DIR%".
    call :maybe_pause %*
    exit /b 1
)

echo [+] Registering 'apm' command for current user...
call :add_to_user_path "%APM_DIR%"
if errorlevel 1 (
    echo [!] Failed to update the user PATH automatically.
    echo [!] Add "%APM_DIR%" to your PATH manually if the 'apm' command is not found.
) else (
    echo [+] PATH updated for the current user.
)

echo.
echo [+] Setup complete! AEngine is ready to use.
echo [+] Restart your terminal or sign in again before using 'apm'.
echo ==========================================
call :maybe_pause %*
exit /b 0

:find_python
for %%V in (3.13 3.12 3.11 3.10) do (
    for /f "usebackq delims=" %%I in (`py -%%V -c "import sys; print(sys.executable)" 2^>nul`) do (
        set "PYTHON_EXE=%%I"
        goto :eof
    )
)
for /f "usebackq delims=" %%I in (`py -3 -c "import sys; print(sys.executable)" 2^>nul`) do (
    set "PYTHON_EXE=%%I"
    goto :eof
)
for /f "usebackq delims=" %%I in (`python -c "import sys; print(sys.executable)" 2^>nul`) do (
    set "PYTHON_EXE=%%I"
    goto :eof
)
goto :eof

:read_python_version
setlocal
set "INTERPRETER=%~1"
set "VERSION="
for /f "usebackq tokens=2 delims= " %%I in (`"%INTERPRETER%" -V 2^>^&1`) do (
    for /f "tokens=1,2 delims=." %%A in ("%%I") do set "VERSION=%%A.%%B"
)
endlocal & set "%~2=%VERSION%"
goto :eof

:is_supported_python
setlocal
set "VERSION=%~1"
for /f "tokens=1,2 delims=." %%A in ("%VERSION%") do (
    set "PY_MAJOR=%%A"
    set "PY_MINOR=%%B"
)

if not "%PY_MAJOR%"=="3" (
    endlocal & exit /b 1
)

if %PY_MINOR% LSS 10 (
    endlocal & exit /b 1
)

if %PY_MINOR% GEQ 14 (
    endlocal & exit /b 1
)

endlocal & exit /b 0

:add_to_user_path
setlocal EnableExtensions DisableDelayedExpansion
set "TARGET_DIR=%~1"
set "USER_PATH="

for /f "skip=2 tokens=2,*" %%A in ('reg query "HKCU\Environment" /v Path 2^>nul') do (
    if /I "%%A"=="REG_SZ" set "USER_PATH=%%B"
    if /I "%%A"=="REG_EXPAND_SZ" set "USER_PATH=%%B"
)

if not defined USER_PATH (
    reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "%TARGET_DIR%" /f >nul 2>&1
    endlocal & exit /b %errorlevel%
)

setlocal EnableDelayedExpansion
set "PATH_CHECK=;!USER_PATH!;"
echo(!PATH_CHECK!| findstr /I /C:";%TARGET_DIR%;" >nul
if not errorlevel 1 (
    endlocal
    endlocal & exit /b 0
)

set "NEW_PATH=!USER_PATH!;%TARGET_DIR%"
reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "!NEW_PATH!" /f >nul 2>&1
set "REG_ERROR=!errorlevel!"
endlocal
endlocal & exit /b %REG_ERROR%

:maybe_pause
if /I "%~1"=="--no-pause" exit /b 0
pause
exit /b 0
