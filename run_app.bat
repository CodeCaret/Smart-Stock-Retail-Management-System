@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
python -m smart_stock_management
deactivate
echo.
echo Press any key to exit ...
pause > nul
