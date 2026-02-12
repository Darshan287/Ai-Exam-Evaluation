@echo off
REM Startup script for AIExamEvaluator
echo ========================================
echo AI Exam Evaluator - Starting Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo [ERROR] Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Display active Python
echo.
echo Active Python:
python --version
echo Python location:
where python
echo.

REM Start Flask application
echo Starting Flask application...
echo Server will run on http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
