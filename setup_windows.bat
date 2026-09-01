@echo off
setlocal
echo [1/3] Creating virtual environment...
python -m venv .venv
if errorlevel 1 goto fail
echo [2/3] Installing packages...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 goto fail
if not exist .env copy .env.example .env
echo [3/3] Setup complete.
echo.
echo Next:
echo 1. Open .env and add GEMINI_API_KEY
echo 2. Run: .venv\Scripts\activate
echo 3. Run: streamlit run app.py
pause
exit /b 0
:fail
echo Setup failed. Check the error above.
pause
exit /b 1
