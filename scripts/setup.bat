@echo off
cd %~dp0
cd ..
pip install -r requirements.txt
set "parent_folder=%cd%"
echo %parent_folder%

xcopy /E /I /Y "%parent_folder%" "%AppData%\apm"
setx PATH "%AppData%\apm;%PATH%" /M
if exist "%AppData%\apm\sources" (
    rd /q /s "%AppData%\apm\sources"
)
exit