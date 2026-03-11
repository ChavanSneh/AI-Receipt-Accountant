@echo off
echo =====================================
echo AI Receipt Accountant - Setup Script
echo =====================================

echo.
echo Checking Python...
python --version
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python first.
    pause
    exit
)

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting Docker backend...
docker compose up -d

echo.
echo Waiting for backend to start...
timeout /t 5

echo.
echo Launching Streamlit UI...
streamlit run ui/dashboard.py

pause