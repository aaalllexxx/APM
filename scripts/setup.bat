@echo off
cd %~dp0
cd ..
pip install -r requirements.txt
set "parent_folder=%cd%"
echo %parent_folder%

xcopy /E /I /Y /EXCLUDE:scripts\xcopy_exclude.txt "%parent_folder%" "%AppData%\apm"
copy /Y "%parent_folder%\apm.ps1" "%AppData%\apm\apm.ps1"

rem Проверяем, есть ли путь уже в PATH
echo %PATH% | find /i "%AppData%\apm" >nul 2>&1
if %errorlevel% neq 0 (
    setx PATH "%AppData%\apm;%PATH%" /M
)

exit