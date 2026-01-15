# Automated PostgreSQL Database Setup
# Uses default PostgreSQL settings (postgres user, localhost, port 5432)

Write-Host "Setting up PostgreSQL Database" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green
Write-Host ""

$psqlPath = "C:\Program Files\PostgreSQL\13\bin\psql.exe"
$dbName = "ai_reviewer_db"
$dbUser = "postgres"
$dbHost = "localhost"
$dbPort = "5432"

# Try to get password from environment or use default
$dbPassword = $env:PGPASSWORD
if (-not $dbPassword) {
    Write-Host "Note: PGPASSWORD environment variable not set." -ForegroundColor Yellow
    Write-Host "Using default connection. You may be prompted for password." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To avoid password prompts, set PGPASSWORD environment variable:" -ForegroundColor Cyan
    Write-Host '  $env:PGPASSWORD = "your_password"' -ForegroundColor White
    Write-Host ""
}

Write-Host "Attempting to create database '$dbName'..." -ForegroundColor Cyan
Write-Host "Using: User=$dbUser, Host=$dbHost, Port=$dbPort" -ForegroundColor Cyan
Write-Host ""

# Check if database exists
$checkResult = & $psqlPath -U $dbUser -h $dbHost -p $dbPort -d postgres -t -c "SELECT 1 FROM pg_database WHERE datname='$dbName';" 2>&1

if ($LASTEXITCODE -eq 0 -and $checkResult -match "1") {
    Write-Host "Database '$dbName' already exists!" -ForegroundColor Yellow
    Write-Host "Skipping creation. Using existing database." -ForegroundColor Green
} else {
    # Create database
    Write-Host "Creating database..." -ForegroundColor Cyan
    $createResult = & $psqlPath -U $dbUser -h $dbHost -p $dbPort -d postgres -c "CREATE DATABASE $dbName;" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Database '$dbName' created successfully!" -ForegroundColor Green
    } else {
        Write-Host "Error creating database:" -ForegroundColor Red
        Write-Host $createResult -ForegroundColor Red
        Write-Host ""
        Write-Host "You may need to:" -ForegroundColor Yellow
        Write-Host "1. Set PGPASSWORD: `$env:PGPASSWORD = 'your_password'" -ForegroundColor White
        Write-Host "2. Or run this manually in pgAdmin:" -ForegroundColor White
        Write-Host "   CREATE DATABASE ai_reviewer_db;" -ForegroundColor White
        exit 1
    }
}

# Update .env file with default connection string
Write-Host ""
Write-Host "Updating backend/.env file..." -ForegroundColor Cyan

$backendEnvPath = Join-Path $PSScriptRoot "backend\.env"

# Read existing .env to preserve other settings
$existingContent = ""
if (Test-Path $backendEnvPath) {
    $existingContent = Get-Content $backendEnvPath -Raw
}

# Create new content
$envContent = @"
# Database
# NOTE: Update the password below with your actual PostgreSQL password
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ai_reviewer_db

# OpenRouter API
OPENROUTER_API_KEY=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

# JWT Secret (generate a new one for production)
JWT_SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
JWT_ALGORITHM=HS256

# CORS
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
"@

Set-Content -Path $backendEnvPath -Value $envContent
Write-Host "Updated backend/.env file!" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT: Update DATABASE_URL in backend/.env with your PostgreSQL password!" -ForegroundColor Yellow
Write-Host "Replace 'YOUR_PASSWORD' with your actual PostgreSQL password." -ForegroundColor Yellow
Write-Host ""
Write-Host "Example:" -ForegroundColor Cyan
Write-Host "DATABASE_URL=postgresql://postgres:mypassword123@localhost:5432/ai_reviewer_db" -ForegroundColor White
Write-Host ""
Write-Host "Database setup complete!" -ForegroundColor Green




