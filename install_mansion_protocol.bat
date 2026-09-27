@echo off
setlocal
cd /d "%~dp0"
set "LAUNCHER=%~dp0launch_mansion.bat"
set "KEY=HKCU\Software\Classes\shiftingmansion"

reg add "%KEY%" /ve /d "URL:Shifting Mansion Protocol" /f >nul
reg add "%KEY%" /v "URL Protocol" /d "" /f >nul

set CMD=%ComSpec% /c call "%LAUNCHER%" "%%1"
reg add "%KEY%\shell\open\command" /ve /d "%CMD%" /f >nul

echo.
echo The Shifting Mansion launcher has been installed for this Windows user.
echo You can now use ENTER MANSION from the dashboard.
echo.
pause
