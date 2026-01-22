# Setup script for OpenWebUI project with uv
# This script initializes the project and installs dependencies

Write-Host "Setting up OpenWebUI project with uv..." -ForegroundColor Green

# Check if uv is installed
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Error: uv is not installed. Please install it first:" -ForegroundColor Red
    Write-Host "  powershell -ExecutionPolicy ByPass -c `"irm https://astral.sh/uv/install.ps1 | iex`"" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
uv venv

# Activate virtual environment and install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
uv pip install open-webui

Write-Host "`nSetup complete! To run OpenWebUI:" -ForegroundColor Green
Write-Host "  1. Activate the virtual environment: .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "  2. Run: open-webui serve" -ForegroundColor Yellow
Write-Host "  Or use the run.ps1 script" -ForegroundColor Yellow
