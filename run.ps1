# Run script for OpenWebUI
# This script activates the virtual environment and launches OpenWebUI

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host "Virtual environment not found. Running setup first..." -ForegroundColor Yellow
    .\setup.ps1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Set data directory (optional - uncomment to customize)
# $env:DATA_DIR = "$PWD\data"
# if (-not (Test-Path $env:DATA_DIR)) {
#     New-Item -ItemType Directory -Path $env:DATA_DIR | Out-Null
# }

Write-Host "Starting OpenWebUI..." -ForegroundColor Green
Write-Host "OpenWebUI will be available at http://localhost:8080" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server`n" -ForegroundColor Yellow

# Run OpenWebUI
open-webui serve
