# Create Database with Password
# Usage: .\create_db_with_password.ps1 -Password "your_password"

param(
    [Parameter(Mandatory=$true)]
    [string]$Password
)

Write-Host "Setting up PostgreSQL Database" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green
Write-Host ""

$psqlPath = "C:\Program Files\PostgreSQL\13\bin\psql.exe"
$dbName = "ai_reviewer_db"
$dbUser = "postgres"
$dbHost = "localhost"
$dbPort = "5432"

# Set password for psql
$env:PGPASSWORD = $Password

Write-Host "Creating database '$dbName'..." -ForegroundColor Cyan

# Check if database exists
$checkResult = & $psqlPath -U $dbUser -h $dbHost -p $dbPort -d postgres -t -c "SELECT 1 FROM pg_database WHERE datname='$dbName';" 2>&1

if ($LASTEXITCODE -eq 0 -and $checkResult -match "1") {
    Write-Host "Database '$dbName' already exists!" -ForegroundColor Yellow
} else {
    # Create database
    $createResult = & $psqlPath -U $dbUser -h $dbHost -p $dbPort -d postgres -c "CREATE DATABASE $dbName;" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Database '$dbName' created successfully!" -ForegroundColor Green
    } else {
        Write-Host "Error: $createResult" -ForegroundColor Red
        exit 1
    }
}

# Update .env file
Write-Host ""
Write-Host "Updating backend/.env file..." -ForegroundColor Cyan

$backendEnvPath = Join-Path $PSScriptRoot "backend\.env"

$envContent = @"
# Database
DATABASE_URL=postgresql://$dbUser`:$Password@$dbHost`:$dbPort/$dbName

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
Write-Host "Updated backend/.env with database connection!" -ForegroundColor Green
Write-Host ""
Write-Host "Database setup complete!" -ForegroundColor Green
Write-Host "You can now start the backend!" -ForegroundColor Cyan




