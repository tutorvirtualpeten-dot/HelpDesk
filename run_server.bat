@echo off
echo Starting HelpDesk System...
call venv\Scripts\activate
python manage.py runserver 0.0.0.0:8000
pause
