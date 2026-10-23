@echo off
setlocal enabledelayedexpansion

title Classical Ciphers & Symmetric Key Cryptography System
color 0B

echo ==============================================================================
echo   CLASSICAL CIPHERS AND SYMMETRIC KEY CRYPTOGRAPHY
echo   Interactive Encryption and Decryption System
echo   College Mini-Project
echo ==============================================================================
echo.

:: Switch to script's directory
cd /d "%~dp0"

:: 1. Check if Python is installed
echo [STEP 1/4] Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    py --version >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        color 0C
        echo [ERROR] Python is not installed or not found in system PATH!
        echo Please install Python 3.9+ from https://www.python.org/
        echo Make sure to check the box "Add Python to PATH" during installation.
        echo.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)
echo [OK] Python is available.
echo.

:: 2. Check and create virtual environment
echo [STEP 2/4] Checking virtual environment (.venv)...
if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Creating new virtual environment in .venv directory...
    %PYTHON_CMD% -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        color 0C
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created successfully.
) else (
    echo [OK] Existing virtual environment found.
)
echo.

:: 3. Install required dependencies
echo [STEP 3/4] Verifying and installing dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo [ERROR] Failed to install required packages!
    pause
    exit /b 1
)
echo [OK] All dependencies (Flask, cryptography) are installed and verified.
echo.

:: 4. Launch web application and browser
echo [STEP 4/4] Starting Cryptography Web Application...
echo.
echo ==============================================================================
echo   Server URL: http://127.0.0.1:5000
echo   Opening browser automatically...
echo   Press CTRL+C in this console to terminate the server.
echo ==============================================================================
echo.

:: Open default browser after a 2-second delay in background
start "" /b cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:5000"

:: Run the Flask application using the virtual environment's python directly
".venv\Scripts\python.exe" app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Server process exited.
    pause
)
