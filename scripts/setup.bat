@echo off
cd ../executable
set "parent_folder=%cd%"
echo %parent_folder%

xcopy /E /I /Y "%parent_folder%" "%AppData%\apm"
setx PATH "%AppData%\apm;%PATH%" /M