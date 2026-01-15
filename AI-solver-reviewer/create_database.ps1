# PostgreSQL Database Creation Script
# This script creates the ai_reviewer_db database

Write-Host "PostgreSQL Database Setup" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green
Write-Host ""

# Common PostgreSQL installation paths
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
        Write-Host "Found PostgreSQL at: $path" -ForegroundColor Green
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
        Write-Host "Path not found. Please create the database manually using pgAdmin." -ForegroundColor Red
        Write-Host ""
        Write-Host "SQL Command to run in pgAdmin:" -ForegroundColor Yellow
        Write-Host "CREATE DATABASE ai_reviewer_db;"
        exit 1
    }
}

Write-Host ""
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

# Check if database already exists
Write-Host ""
Write-Host "Checking if database exists..." -ForegroundColor Cyan
$env:PGPASSWORD = $dbPasswordPlain
$checkDbCommand = "SELECT 1 FROM pg_database WHERE datname='$dbName';"

$dbExists = & $psqlPath -h $dbHost -p $dbPort -U $dbUser -d postgres -t -c $checkDbCommand 2>&1

if ($dbExists -match "1") {
    Write-Host "Database '$dbName' already exists!" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to recreate it? (y/N)"
    if ($overwrite -eq "y" -or $overwrite -eq "Y") {
        Write-Host "Dropping existing database..." -ForegroundColor Cyan
        & $psqlPath -h $dbHost -p $dbPort -U $dbUser -d postgres -c "DROP DATABASE $dbName;" 2>&1 | Out-Null
    } else {
        Write-Host "Using existing database." -ForegroundColor Green
    }
}

# Create database
if (-not ($dbExists -match "1" -and ($overwrite -ne "y" -and $overwrite -ne "Y"))) {
    Write-Host "Creating database '$dbName'..." -ForegroundColor Cyan
    $createDbCommand = "CREATE DATABASE $dbName;"
    
    try {
        $result = & $psqlPath -h $dbHost -p $dbPort -U $dbUser -d postgres -c $createDbCommand 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Database created successfully!" -ForegroundColor Green
        } else {
            Write-Host "Error: $result" -ForegroundColor Red
            Write-Host "You may need to create the database manually." -ForegroundColor Yellow
        }
    } catch {
        Write-Host "Error creating database: $_" -ForegroundColor Red
        Write-Host "SQL Command to run manually: $createDbCommand" -ForegroundColor Yellow
    }
}

# Update .env file
Write-Host ""
Write-Host "Updating backend/.env file..." -ForegroundColor Cyan

$backendEnvPath = Join-Path $PSScriptRoot "backend\.env"
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

Set-Content -Path $backendEnvPath -Value $envContent
Write-Host "Updated backend/.env with your database connection!" -ForegroundColor Green

Write-Host ""
Write-Host "Database setup complete!" -ForegroundColor Green
Write-Host "You can now start the backend with: python run.py" -ForegroundColor Cyan


