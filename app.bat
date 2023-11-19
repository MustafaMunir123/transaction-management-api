@echo off
for /f "tokens=5" %%a in ('netstat -aon ^| find "8000"') do taskkill /f /pid %%a
timeout /t 2
start "" "C:\WINDOWS\system32\notepad.exe"
cd /d "d:\ned_assignment\PlutoSols\transaction_management_api"
START /B python manage.py runserver
