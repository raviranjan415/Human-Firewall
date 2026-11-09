@echo off
echo =========================================================
echo   Starting Human Firewall Platform (Flask + SQLite)
echo   Local Address: http://127.0.0.1:5000
echo =========================================================
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe run.py
) else (
    python run.py
)
pause

