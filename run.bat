@echo off
REM run.bat - create/activate venv, install deps, run github_follow_compare.py
REM Usage: run.bat <githubUsername> [--no-gui --csv out.csv --filters filters.example.json ...]

REM Move to script directory (project root)
cd /d "%~dp0"

set VENV_DIR=.venv

REM Create venv if missing
if not exist "%VENV_DIR%" (
    echo Creating virtual environment in %VENV_DIR%...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Failed to create virtual environment. Ensure Python is on PATH.
        exit /b 1
    )
)

REM Activate venv for cmd.exe
if exist "%VENV_DIR%\Scripts\activate.bat" (
    call "%VENV_DIR%\Scripts\activate.bat"
) else (
    echo Activation script not found. Virtual environment may be invalid.
    exit /b 1
)

REM Ensure pip is available and optionally install requirements
if exist "requirements.txt" (
    echo Installing requirements from requirements.txt...
    "%VENV_DIR%\Scripts\python.exe" -m pip install --upgrade pip
    "%VENV_DIR%\Scripts\python.exe" -m pip install -r requirements.txt
)

REM Run the main script forwarding all arguments
echo Running github_follow_compare.py %*
"%VENV_DIR%\Scripts\python.exe" github_follow_compare.py %*

REM Deactivate venv (optional)
if defined VIRTUAL_ENV (
    call "%VENV_DIR%\Scripts\deactivate.bat"
)

exit /b 0