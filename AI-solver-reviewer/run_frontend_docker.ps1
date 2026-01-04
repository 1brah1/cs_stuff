# Docker Frontend Setup Script
# This script sets up and runs the frontend using Docker

Write-Host "Setting up Frontend with Docker" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green
Write-Host ""

# Check if Docker is running
$dockerRunning = docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

Write-Host "Docker is running!" -ForegroundColor Green
Write-Host ""

# Navigate to frontend directory
$frontendPath = Join-Path $PSScriptRoot "frontend"
Set-Location $frontendPath

Write-Host "Building frontend Docker image..." -ForegroundColor Cyan
docker build -t ai-reviewer-frontend .

if ($LASTEXITCODE -eq 0) {
    Write-Host "Frontend image built successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Starting frontend container..." -ForegroundColor Cyan
    Write-Host "Frontend will be available at: http://localhost:3000" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press Ctrl+C to stop the container" -ForegroundColor Yellow
    Write-Host ""
    
    # Run the container
    docker run -it --rm `
        -p 3000:3000 `
        -v "${PWD}:/app" `
        -v "/app/node_modules" `
        -e REACT_APP_API_URL=http://localhost:8000 `
        ai-reviewer-frontend
} else {
    Write-Host "Failed to build Docker image." -ForegroundColor Red
    exit 1
}

