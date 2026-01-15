# Deploy to EC2 - Run this FROM your local Windows machine

# Configuration - UPDATE THESE VALUES
$EC2_IP = "YOUR_EC2_IP_HERE"
$EC2_USER = "ubuntu"
$KEY_FILE = "ai-reviewer-key.pem"
$OPENROUTER_KEY = "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"
$JWT_SECRET = -join ((48..57) + (97..102) | Get-Random -Count 32 | ForEach-Object {[char]$_})

Write-Host "🚀 Deploying AI-Reviewer to EC2..." -ForegroundColor Green

# Copy files to EC2
Write-Host "📤 Copying files to EC2..." -ForegroundColor Cyan
scp -i $KEY_FILE -r backend docker-compose.prod.yml ${EC2_USER}@${EC2_IP}:~/ai-reviewer/

# Deploy on EC2
Write-Host "🔧 Setting up and starting services..." -ForegroundColor Cyan
$commands = @"
cd ~/ai-reviewer
cat > .env << 'ENVEOF'
OPENROUTER_API_KEY=$OPENROUTER_KEY
JWT_SECRET_KEY=$JWT_SECRET
GITHUB_USERNAME=your-username
ENVEOF
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
docker-compose -f docker-compose.prod.yml up -d
echo ""
echo "✅ Deployment complete!"
"@

ssh -i $KEY_FILE ${EC2_USER}@$EC2_IP $commands

Write-Host ""
Write-Host "✅ Deployment finished!" -ForegroundColor Green
Write-Host "🌐 Backend: http://${EC2_IP}:8000" -ForegroundColor Yellow
Write-Host "📚 API Docs: http://${EC2_IP}:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔍 Testing health endpoint..." -ForegroundColor Cyan
Start-Sleep -Seconds 5
try {
    $response = Invoke-WebRequest -Uri "http://${EC2_IP}:8000/health" -UseBasicParsing
    Write-Host "✅ Health check passed!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Service starting... wait 30s and try: curl http://${EC2_IP}:8000/health" -ForegroundColor Yellow
}
