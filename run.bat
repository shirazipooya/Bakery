@echo off
cd /d "%~dp0"
.\.venv\Scripts\python.exe -m waitress --host=127.0.0.1 --port=5000 app:app
pause