@echo off
REM Installation script for Planner Task Creator CLI + MCP Server
REM Windows Batch version
REM
REM Usage: scripts\INSTALLATION.bat
REM Run from the project root directory

setlocal enabledelayedexpansion

echo ==========================================
echo Planner Task Creator CLI + MCP Server
echo Installation Script (Windows)
echo ==========================================
echo.

REM Get script directory and project root
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
pushd "%PROJECT_ROOT%"
set "PROJECT_ROOT=%CD%"
popd

REM Check Python
echo Checking Python installation...
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PYTHON_CMD=python"
) else (
    where python3 >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        set "PYTHON_CMD=python3"
    ) else (
        echo [ERROR] Python is not installed
        echo Please install Python 3.8 or later from https://python.org
        echo Make sure to check 'Add Python to PATH' during installation
        exit /b 1
    )
)

for /f "tokens=*" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] %PYTHON_VERSION% found

REM Check pip
echo Checking pip installation...
%PYTHON_CMD% -m pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] pip is not installed
    echo Please reinstall Python and ensure pip is included
    exit /b 1
)
echo [OK] pip found

REM Check Node.js (optional)
echo.
echo Checking Node.js installation (for MCP server)...
set "INSTALL_MCP=0"
where node >nul 2>&1
if %ERRORLEVEL% equ 0 (
    for /f "tokens=*" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
    echo [OK] Node.js !NODE_VERSION! found
    set "INSTALL_MCP=1"
) else (
    echo [WARN] Node.js not found - MCP server will not be installed
    echo        Install from https://nodejs.org if you want MCP server support
)

REM Create .planner-cli directory
echo.
echo Creating .planner-cli directory...
set "PLANNER_CLI_DIR=%USERPROFILE%\.planner-cli"
if not exist "%PLANNER_CLI_DIR%" mkdir "%PLANNER_CLI_DIR%"
echo [OK] Directory created: %PLANNER_CLI_DIR%

REM Create virtual environment
echo.
echo Setting up Python virtual environment...
set "VENV_PATH=%PROJECT_ROOT%\venv"

if exist "%VENV_PATH%" (
    echo [WARN] Virtual environment already exists, recreating...
    rmdir /s /q "%VENV_PATH%"
)

%PYTHON_CMD% -m venv "%VENV_PATH%"
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Error creating virtual environment
    exit /b 1
)
echo [OK] Virtual environment created at: %VENV_PATH%

REM Activate virtual environment and install dependencies
echo.
echo Installing Python dependencies in virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"

REM Upgrade pip
%PYTHON_CMD% -m pip install --upgrade pip >nul 2>&1

REM Install requirements
%PYTHON_CMD% -m pip install -r "%PROJECT_ROOT%\requirements.txt"
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Error installing Python dependencies
    call deactivate
    exit /b 1
)
echo [OK] Python dependencies installed

REM Copy CLI to .planner-cli
echo.
echo Installing Python CLI...
copy /Y "%PROJECT_ROOT%\planner.py" "%PLANNER_CLI_DIR%\" >nul

REM Copy planner_lib folder
if exist "%PLANNER_CLI_DIR%\planner_lib" rmdir /s /q "%PLANNER_CLI_DIR%\planner_lib"
xcopy /E /I /Q /Y "%PROJECT_ROOT%\planner_lib" "%PLANNER_CLI_DIR%\planner_lib" >nul

echo [OK] CLI installed to %PLANNER_CLI_DIR%

call deactivate

REM Install MCP server
if "%INSTALL_MCP%"=="1" (
    echo.
    set /p INSTALL_MCP_RESPONSE="Install MCP server? (y/n): "
    if /i "!INSTALL_MCP_RESPONSE!"=="y" (
        echo Installing Node.js dependencies...
        pushd "%PROJECT_ROOT%"
        call npm install

        echo Building TypeScript...
        call npm run build

        if exist "%PROJECT_ROOT%\dist\server.js" (
            echo [OK] MCP server built successfully
        ) else (
            echo [ERROR] Error building MCP server
        )
        popd
    )
)

REM Configuration
echo.
echo ==========================================
echo Configuration Setup
echo ==========================================
echo.
echo You need Azure AD credentials to use this CLI.
echo Please have your TENANT_ID and CLIENT_ID ready.
echo.
set /p CONFIGURE_RESPONSE="Configure now? (y/n): "

if /i "%CONFIGURE_RESPONSE%"=="y" (
    set /p TENANT_ID="Enter your TENANT_ID: "
    set /p CLIENT_ID="Enter your CLIENT_ID: "

    REM Create config file
    set "CONFIG_PATH=%PLANNER_CLI_DIR%\config.json"
    (
        echo {
        echo   "tenant_id": "!TENANT_ID!",
        echo   "client_id": "!CLIENT_ID!"
        echo }
    ) > "!CONFIG_PATH!"

    echo [OK] Configuration saved to !CONFIG_PATH!

    echo.
    set /p TEST_AUTH_RESPONSE="Test authentication now? (y/n): "
    if /i "!TEST_AUTH_RESPONSE!"=="y" (
        call "%VENV_PATH%\Scripts\activate.bat"
        %PYTHON_CMD% "%PLANNER_CLI_DIR%\planner.py" init-auth
        call deactivate
    )
) else (
    echo.
    echo To configure later, create %PLANNER_CLI_DIR%\config.json with:
    echo {
    echo   "tenant_id": "your-tenant-id",
    echo   "client_id": "your-client-id"
    echo }
    echo.
    echo Or set environment variables:
    echo set TENANT_ID=your-tenant-id
    echo set CLIENT_ID=your-client-id
)

REM Final instructions
echo.
echo ==========================================
echo Installation Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Activate virtual environment:
echo    venv\Scripts\activate.bat
echo.
echo 2. Authenticate:
echo    python planner.py init-auth
echo.
echo 3. Set defaults:
echo    python planner.py set-defaults --plan "My Plan" --bucket "To Do"
echo.
echo 4. Create a task:
echo    python planner.py add --title "My first task"
echo.
echo Note: Always activate the virtual environment before using the CLI:
echo   venv\Scripts\activate.bat
echo.
echo For help: python planner.py --help
echo Documentation: type README.md
echo.
echo Happy planning!

endlocal
