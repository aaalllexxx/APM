@echo off
echo waiting script close...
TIMEOUT /T 3
rd /q /s "%AppData%\apm\sources"