@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -3.11 -m venv .venv
  if errorlevel 1 (echo Install Python 3.11+ first.& pause & exit /b 1)
)
".venv\Scripts\python.exe" -m pip install -r backend\requirements.txt
if errorlevel 1 (echo Dependency installation failed.& pause & exit /b 1)
".venv\Scripts\python.exe" -m uvicorn backend.app:app --host 127.0.0.1 --port 8765
pause
