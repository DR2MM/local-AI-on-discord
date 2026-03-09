@echo off

echo Creating virtual environment...
python -m venv .venv
echo Done.
echo Activating environment...
call .venv\Scripts\activate
echo Done.
echo Installing dependencies...
pip install -r requirements.txt
echo Done.
pause