# Setup script for AI Document Reviewer
# This script creates the necessary .env files

Write-Host "Setting up AI Document Reviewer..." -ForegroundColor Green

# Get API key from user
$openrouterKey = Read-Host "Enter your OpenRouter API Key"

# Backend .env file
$backendEnvPath = "AI-solver-reviewer\backend\.env"
$backendEnvContent = @"
# Database
DATABASE_URL=sqlite:///./data/ai_reviewer.db

# OpenRouter API
OPENROUTER_API_KEY=$openrouterKey

# JWT Secret (generate a new one for production)
JWT_SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
JWT_ALGORITHM=HS256

# CORS
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
"@

if (Test-Path $backendEnvPath) {
    Write-Host "Backend .env file already exists. Skipping..." -ForegroundColor Yellow
} else {
    Set-Content -Path $backendEnvPath -Value $backendEnvContent
    Write-Host "Created backend/.env file" -ForegroundColor Green
}

# Frontend .env file
$frontendEnvPath = "AI-solver-reviewer\frontend\.env"
$frontendEnvContent = "REACT_APP_API_URL=http://localhost:8000"

if (Test-Path $frontendEnvPath) {
    Write-Host "Frontend .env file already exists. Skipping..." -ForegroundColor Yellow
} else {
    Set-Content -Path $frontendEnvPath -Value $frontendEnvContent
    Write-Host "Created frontend/.env file" -ForegroundColor Green
}

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Install backend dependencies: cd AI-solver-reviewer\backend && pip install -r requirements.txt"
Write-Host "2. Install frontend dependencies: cd AI-solver-reviewer\frontend && npm install"
Write-Host "3. Start backend: cd AI-solver-reviewer\backend && python run.py"
Write-Host "4. Start frontend: cd AI-solver-reviewer\frontend && npm start"
