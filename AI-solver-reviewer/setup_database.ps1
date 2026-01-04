# PostgreSQL Database Setup Script
# This script helps you set up the database for AI Document Reviewer

Write-Host "PostgreSQL Database Setup" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green
Write-Host ""

# Common PostgreSQL installation paths on Windows
$pgPaths = @(
    "C:\Program Files\PostgreSQL\16\bin\psql.exe",
    "C:\Program Files\PostgreSQL\15\bin\psql.exe",
    "C:\Program Files\PostgreSQL\14\bin\psql.exe",
    "C:\Program Files\PostgreSQL\13\bin\psql.exe",
    "C:\Program Files (x86)\PostgreSQL\16\bin\psql.exe",
    "C:\Program Files (x86)\PostgreSQL\15\bin\psql.exe"
)

$psqlPath = $null
foreach ($path in $pgPaths) {
    if (Test-Path $path) {
        $psqlPath = $path
        break
    }
}

if (-not $psqlPath) {
    Write-Host "Could not find psql.exe automatically." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please provide your PostgreSQL installation path:" -ForegroundColor Cyan
    Write-Host "Example: C:\Program Files\PostgreSQL\16\bin\psql.exe"
    $customPath = Read-Host "Enter path to psql.exe"
    if (Test-Path $customPath) {
        $psqlPath = $customPath
    } else {
        Write-Host "Path not found. Please run the SQL commands manually." -ForegroundColor Red
        Write-Host ""
        Write-Host "SQL Commands to run:" -ForegroundColor Yellow
        Write-Host "CREATE DATABASE ai_reviewer_db;"
        exit 1
    }
}

Write-Host "Found PostgreSQL at: $psqlPath" -ForegroundColor Green
Write-Host ""

# Get database connection details
Write-Host "Please provide your PostgreSQL connection details:" -ForegroundColor Cyan
$dbUser = Read-Host "Database username (default: postgres)"
if ([string]::IsNullOrWhiteSpace($dbUser)) {
    $dbUser = "postgres"
}

$dbPassword = Read-Host "Database password" -AsSecureString
$dbPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassword)
)

$dbHost = Read-Host "Database host (default: localhost)"
if ([string]::IsNullOrWhiteSpace($dbHost)) {
    $dbHost = "localhost"
}

$dbPort = Read-Host "Database port (default: 5432)"
if ([string]::IsNullOrWhiteSpace($dbPort)) {
    $dbPort = "5432"
}

$dbName = "ai_reviewer_db"

# Create database
Write-Host ""
Write-Host "Creating database '$dbName'..." -ForegroundColor Cyan

$env:PGPASSWORD = $dbPasswordPlain
$createDbCommand = "CREATE DATABASE $dbName;"

try {
    & $psqlPath -h $dbHost -p $dbPort -U $dbUser -d postgres -c $createDbCommand
    Write-Host "Database created successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error creating database. You may need to run this manually." -ForegroundColor Red
    Write-Host "SQL Command: $createDbCommand" -ForegroundColor Yellow
}

# Update .env file
Write-Host ""
Write-Host "Updating backend/.env file..." -ForegroundColor Cyan

$envContent = @"
# Database
DATABASE_URL=postgresql://$dbUser`:$dbPasswordPlain@$dbHost`:$dbPort/$dbName

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

Set-Content -Path "backend\.env" -Value $envContent
Write-Host "Updated backend/.env with your database connection!" -ForegroundColor Green

Write-Host ""
Write-Host "Setup complete! You can now start the backend." -ForegroundColor Green
Write-Host "Run: cd backend && python run.py" -ForegroundColor Cyan

