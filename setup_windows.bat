@echo off

echo Creating virtual environment...
python -m venv .venv
echo Activating environment...
call .venv\Scripts\activate
echo Installing dependencies...
pip install -r requirements.txt
echo Done.
pause
