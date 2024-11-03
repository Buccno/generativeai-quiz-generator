@echo off
echo Checking Python version...

python --version | findstr "3.10" >nul
if %errorlevel% neq 0 (
    echo Python 3.10 or higher is required. Please install Python 3.10.
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt

echo Running the project...
python src/gemini-quiz-generator.py
pause
