@echo off
echo waiting script close...
TIMEOUT /T 10
rd /q /s "%AppData%\apm\sources"