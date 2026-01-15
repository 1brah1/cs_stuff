# EC2 Deployment Script
# Run this from your local machine to deploy to EC2

param(
    [Parameter(Mandatory = $true)]
    [string]$EC2_IP,
    
    [Parameter(Mandatory = $true)]
    [string]$KeyFile,
    
    [Parameter(Mandatory = $true)]
    [string]$OpenRouterKey
)

$EC2_USER = "ubuntu"
# Fixed JWT Secret as requested
$JWT_SECRET = "c378a55a01406ef0b4a80b152311d79e00e74cd81b6944045b236f34654e7cfc"

Write-Host "Deploying AI-Reviewer to EC2: $EC2_IP" -ForegroundColor Green

# 0. Check if key file exists
if (!(Test-Path $KeyFile)) {
    Write-Error "Error: Key file not found at $KeyFile"
    exit 1
}

# 1. Prepare remote directory (Nuclear cleanup to fix permission issues)
Write-Host "Preparing remote directory..." -ForegroundColor Cyan
# Using sudo because Docker may have created files owned by root
ssh -i $KeyFile -o StrictHostKeyChecking=no -o ConnectTimeout=15 ${EC2_USER}@${EC2_IP} "sudo rm -rf ~/ai-reviewer/backend; mkdir -p ~/ai-reviewer"

# 2. Create local .env file temporarily
Write-Host "Generating environment configuration..." -ForegroundColor Cyan
$envContent = @"
OPENROUTER_API_KEY=$OpenRouterKey
JWT_SECRET_KEY=$JWT_SECRET
DATABASE_URL=sqlite:///./data/ai_reviewer.db
FRONTEND_URL=https://1brah1.github.io
ENVIRONMENT=production
"@
$localEnvPath = Join-Path $PSScriptRoot ".env.prod"
$envContent | Out-File -FilePath $localEnvPath -Encoding ascii

# 3. Copy files to EC2
Write-Host "Copying files to EC2..." -ForegroundColor Cyan
$localBackend = Join-Path $PSScriptRoot "backend"
$localDocker = Join-Path $PSScriptRoot "docker-compose.prod.yml"

# Copy backend, docker-compose and the generated .env
# Removed verbose (-v) to make output cleaner, added robust pathing
scp -i $KeyFile -o StrictHostKeyChecking=no -o ConnectTimeout=10 -r "$localBackend" "$localDocker" "$localEnvPath" "${EC2_USER}@${EC2_IP}:~/ai-reviewer/"

# 4. Clean up local temp file
Remove-Item $localEnvPath -ErrorAction SilentlyContinue

# 5. Start services on EC2
Write-Host "Starting services on EC2..." -ForegroundColor Cyan
ssh -i $KeyFile -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} "cd ~/ai-reviewer; mv .env.prod .env; docker-compose -f docker-compose.prod.yml down; docker-compose -f docker-compose.prod.yml up -d --build"

Write-Host ""
Write-Host "Deployment finished!" -ForegroundColor Green
Write-Host "Backend: http://${EC2_IP}:8000" -ForegroundColor Yellow
Write-Host "API Docs: http://${EC2_IP}:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Testing health endpoint..." -ForegroundColor Cyan
Start-Sleep -Seconds 15
try {
    $response = Invoke-WebRequest -Uri "http://${EC2_IP}:8000/health" -UseBasicParsing -TimeoutSec 10
    Write-Host "Health check passed!" -ForegroundColor Green
}
catch {
    Write-Host "Service starting... wait 30s and try: curl http://${EC2_IP}:8000/health" -ForegroundColor Yellow
}
