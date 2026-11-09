@echo off
echo =========================================================
echo   Human Firewall — AWS Real Cloud Deployment Wizard
echo =========================================================
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe scripts\aws_deployer.py
) else (
    python scripts\aws_deployer.py
)
pause

