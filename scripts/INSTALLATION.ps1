# Installation script for Planner Task Creator CLI + MCP Server
# Windows PowerShell version
#
# Usage: .\scripts\INSTALLATION.ps1
# Note: You may need to run: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Planner Task Creator CLI + MCP Server" -ForegroundColor Cyan
Write-Host "Installation Script (Windows)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Helper function to check command existence
function Test-Command {
    param([string]$Command)
    $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
}

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonCmd = $null
if (Test-Command "python") {
    $pythonCmd = "python"
} elseif (Test-Command "python3") {
    $pythonCmd = "python3"
}

if (-not $pythonCmd) {
    Write-Host "Error: Python is not installed" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or later from https://python.org" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    exit 1
}

$pythonVersionOutput = & $pythonCmd --version 2>&1
Write-Host "[OK] $pythonVersionOutput found" -ForegroundColor Green

# Validate Python version (3.8+)
$versionMatch = [regex]::Match($pythonVersionOutput, "Python (\d+)\.(\d+)")
if ($versionMatch.Success) {
    $major = [int]$versionMatch.Groups[1].Value
    $minor = [int]$versionMatch.Groups[2].Value
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
        Write-Host "Error: Python 3.8 or later is required (found $major.$minor)" -ForegroundColor Red
        exit 1
    }
}

# Check pip
Write-Host "Checking pip installation..." -ForegroundColor Yellow
$pipOutput = & $pythonCmd -m pip --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: pip is not installed" -ForegroundColor Red
    Write-Host "Please reinstall Python and ensure pip is included" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] pip found" -ForegroundColor Green

# Check Node.js (optional)
Write-Host ""
Write-Host "Checking Node.js installation (for MCP server)..." -ForegroundColor Yellow
$installMcp = $false
if (Test-Command "node") {
    $nodeVersion = & node --version 2>&1
    Write-Host "[OK] Node.js $nodeVersion found" -ForegroundColor Green

    # Also check for npm
    if (Test-Command "npm") {
        $npmVersion = & npm --version 2>&1
        Write-Host "[OK] npm $npmVersion found" -ForegroundColor Green
        $installMcp = $true
    } else {
        Write-Host "[WARN] npm not found - MCP server will not be installed" -ForegroundColor Yellow
        Write-Host "  npm should come with Node.js. Try reinstalling Node.js" -ForegroundColor Yellow
    }
} else {
    Write-Host "[WARN] Node.js not found - MCP server will not be installed" -ForegroundColor Yellow
    Write-Host "  Install from https://nodejs.org if you want MCP server support" -ForegroundColor Yellow
}

# Create .planner-cli directory
Write-Host ""
Write-Host "Creating .planner-cli directory..." -ForegroundColor Yellow
$plannerCliDir = Join-Path $env:USERPROFILE ".planner-cli"
if (-not (Test-Path $plannerCliDir)) {
    New-Item -ItemType Directory -Path $plannerCliDir -Force | Out-Null
}
Write-Host "[OK] Directory created: $plannerCliDir" -ForegroundColor Green

# Create virtual environment
Write-Host ""
Write-Host "Setting up Python virtual environment..." -ForegroundColor Yellow
$venvPath = Join-Path (Join-Path $PSScriptRoot "..") "venv"
$venvPath = [System.IO.Path]::GetFullPath($venvPath)

if (Test-Path $venvPath) {
    Write-Host "[WARN] Virtual environment already exists, recreating..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $venvPath
}

& $pythonCmd -m venv $venvPath
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error creating virtual environment" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Virtual environment created at: $venvPath" -ForegroundColor Green

# Activate virtual environment and install dependencies
Write-Host ""
Write-Host "Installing Python dependencies in virtual environment..." -ForegroundColor Yellow
$activateScript = Join-Path $venvPath "Scripts" "Activate.ps1"

# Source the activation script
. $activateScript

# Upgrade pip (suppress output)
& $pythonCmd -m pip install --upgrade pip 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Could not upgrade pip" -ForegroundColor Yellow
}

# Install requirements
$requirementsPath = Join-Path (Join-Path $PSScriptRoot "..") "requirements.txt"
$requirementsPath = [System.IO.Path]::GetFullPath($requirementsPath)
& $pythonCmd -m pip install -r $requirementsPath

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error installing Python dependencies" -ForegroundColor Red
    deactivate
    exit 1
}
Write-Host "[OK] Python dependencies installed" -ForegroundColor Green

# Copy planner.py and planner_lib to .planner-cli
Write-Host ""
Write-Host "Installing Python CLI..." -ForegroundColor Yellow
$projectRoot = Join-Path $PSScriptRoot ".."
$projectRoot = [System.IO.Path]::GetFullPath($projectRoot)

$plannerPy = Join-Path $projectRoot "planner.py"
Copy-Item -Path $plannerPy -Destination $plannerCliDir -Force

# Copy planner_lib folder
$plannerLib = Join-Path $projectRoot "planner_lib"
$plannerLibDest = Join-Path $plannerCliDir "planner_lib"
if (Test-Path $plannerLibDest) {
    Remove-Item -Recurse -Force $plannerLibDest
}
Copy-Item -Path $plannerLib -Destination $plannerLibDest -Recurse

Write-Host "[OK] CLI installed to $plannerCliDir" -ForegroundColor Green

# Deactivate virtual environment
deactivate

# Install MCP server
if ($installMcp) {
    Write-Host ""
    $response = Read-Host "Install MCP server? (y/n)"
    if ($response -match "^[Yy]") {
        Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
        Push-Location $projectRoot

        & npm install
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error installing Node.js dependencies" -ForegroundColor Red
            Pop-Location
        } else {
            Write-Host "[OK] Node.js dependencies installed" -ForegroundColor Green

            Write-Host "Building TypeScript..." -ForegroundColor Yellow
            & npm run build

            $serverJs = Join-Path $projectRoot "dist" "server.js"
            if (Test-Path $serverJs) {
                Write-Host "[OK] MCP server built successfully" -ForegroundColor Green
            } else {
                Write-Host "Error building MCP server" -ForegroundColor Red
            }
            Pop-Location
        }
    }
}

# Configuration
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Configuration Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You need Azure AD credentials to use this CLI."
Write-Host "Please have your TENANT_ID and CLIENT_ID ready."
Write-Host ""
$response = Read-Host "Configure now? (y/n)"

if ($response -match "^[Yy]") {
    $tenantId = Read-Host "Enter your TENANT_ID"
    $clientId = Read-Host "Enter your CLIENT_ID"

    # Create config file (UTF-8 without BOM for JSON compatibility)
    $configPath = Join-Path $plannerCliDir "config.json"
    $config = @{
        tenant_id = $tenantId
        client_id = $clientId
    } | ConvertTo-Json

    # Write without BOM (compatible with all PowerShell versions)
    [System.IO.File]::WriteAllText($configPath, $config, [System.Text.UTF8Encoding]::new($false))
    Write-Host "[OK] Configuration saved to $configPath" -ForegroundColor Green

    # Test authentication
    Write-Host ""
    $response = Read-Host "Test authentication now? (y/n)"
    if ($response -match "^[Yy]") {
        . $activateScript
        & $pythonCmd (Join-Path $plannerCliDir "planner.py") init-auth
        deactivate
    }
} else {
    Write-Host ""
    Write-Host "To configure later, create $plannerCliDir\config.json with:" -ForegroundColor Yellow
    Write-Host '{' -ForegroundColor Gray
    Write-Host '  "tenant_id": "your-tenant-id",' -ForegroundColor Gray
    Write-Host '  "client_id": "your-client-id"' -ForegroundColor Gray
    Write-Host '}' -ForegroundColor Gray
    Write-Host ""
    Write-Host "Or set environment variables:" -ForegroundColor Yellow
    Write-Host '$env:TENANT_ID = "your-tenant-id"' -ForegroundColor Gray
    Write-Host '$env:CLIENT_ID = "your-client-id"' -ForegroundColor Gray
}

# Final instructions
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Activate virtual environment:" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Authenticate:" -ForegroundColor White
Write-Host "   python planner.py init-auth" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Set defaults:" -ForegroundColor White
Write-Host '   python planner.py set-defaults --plan "My Plan" --bucket "To Do"' -ForegroundColor Gray
Write-Host ""
Write-Host "4. Create a task:" -ForegroundColor White
Write-Host '   python planner.py add --title "My first task"' -ForegroundColor Gray
Write-Host ""
Write-Host "Note: Always activate the virtual environment before using the CLI:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "For help: python planner.py --help" -ForegroundColor White
Write-Host "Documentation: Get-Content README.md" -ForegroundColor White
Write-Host ""
Write-Host "Happy planning!" -ForegroundColor Green
