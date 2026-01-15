# EC2 Deployment Script
# Run this from your local machine to deploy to EC2

param(
    [Parameter(Mandatory=$true)]
    [string]$EC2_IP,
    
    [Parameter(Mandatory=$true)]
    [string]$KeyFile,
    
    [Parameter(Mandatory=$true)]
    [string]$OpenRouterKey
)

$EC2_USER = "ubuntu"
$JWT_SECRET = -join ((48..57) + (97..102) | Get-Random -Count 32 | ForEach-Object {[char]$_})

Write-Host "🚀 Deploying AI-Reviewer to EC2: $EC2_IP" -ForegroundColor Green

# Copy files to EC2
Write-Host "📤 Copying files to EC2..." -ForegroundColor Cyan
scp -i $KeyFile -r AI-solver-reviewer/backend AI-solver-reviewer/docker-compose.prod.yml ${EC2_USER}@${EC2_IP}:~/ai-reviewer/

# Deploy on EC2
Write-Host "🔧 Starting services..." -ForegroundColor Cyan
ssh -i $KeyFile ${EC2_USER}@${EC2_IP} @"
cd ~/ai-reviewer
cat > .env << 'EOF'
OPENROUTER_API_KEY=$OpenRouterKey
JWT_SECRET_KEY=$JWT_SECRET
DATABASE_URL=sqlite:///./data/ai_reviewer.db
EOF
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
"@

Write-Host ""
Write-Host "✅ Deployment finished!" -ForegroundColor Green
Write-Host "🌐 Backend: http://${EC2_IP}:8000" -ForegroundColor Yellow
Write-Host "📚 API Docs: http://${EC2_IP}:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔍 Testing health endpoint..." -ForegroundColor Cyan
Start-Sleep -Seconds 10
try {
    $response = Invoke-WebRequest -Uri "http://${EC2_IP}:8000/health" -UseBasicParsing
    Write-Host "✅ Health check passed!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Service starting... wait 30s and try: curl http://${EC2_IP}:8000/health" -ForegroundColor Yellow
}
