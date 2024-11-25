@echo off
cd /d "%~dp0"
@REM start "" /min .\python\python.exe -m waitress --host=127.0.0.1 --port=5000 app:app
start "" /min .\python\python.exe .\run.py
timeout /t 10 /nobreak >nul
start "" /min "http://127.0.0.1:5000"
exit