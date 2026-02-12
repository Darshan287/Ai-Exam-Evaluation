# Startup script for AIExamEvaluator
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Exam Evaluator - Starting Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created." -ForegroundColor Green
    Write-Host ""
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Display active Python
Write-Host ""
Write-Host "Active Python:" -ForegroundColor Green
python --version
Write-Host "Python location:" -ForegroundColor Green
Get-Command python | Select-Object -ExpandProperty Source
Write-Host ""

# Start Flask application
Write-Host "Starting Flask application..." -ForegroundColor Green
Write-Host "Server will run on http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
python app.py
