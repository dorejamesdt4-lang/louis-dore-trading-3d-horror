@echo off
setlocal
cd /d "%~dp0"
python main.py
if errorlevel 1 (
  echo.
  echo The Shifting Mansion could not start.
  echo Make sure Python 3.12 or 3.13 and the requirements are installed.
  pause
)
