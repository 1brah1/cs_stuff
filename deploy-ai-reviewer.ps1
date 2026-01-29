# Quick Deployment to EC2

# This script helps you deploy the AI Document Reviewer to EC2

Write-Host "AI Document Reviewer - EC2 Deployment Helper" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

$EC2_HOST = "13.211.53.117"
$EC2_USER = "ubuntu"
$SSH_KEY = "C:\Users\ibrah\OneDrive\Documents\Gaylord.pem"

Write-Host "EC2 Instance: $EC2_USER@$EC2_HOST" -ForegroundColor Yellow
Write-Host "SSH Key: $SSH_KEY" -ForegroundColor Yellow
Write-Host ""

# Check if SSH key exists
if (-not (Test-Path $SSH_KEY)) {
    Write-Host "ERROR: SSH key not found at $SSH_KEY" -ForegroundColor Red
    exit 1
}

Write-Host "What would you like to deploy?" -ForegroundColor Green
Write-Host "1. Backend only" -ForegroundColor White
Write-Host "2. Simple Frontend only" -ForegroundColor White
Write-Host "3. Both Backend and Frontend" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-3)"

switch ($choice) {
    "1" {
        Write-Host "`nDeploying Backend..." -ForegroundColor Cyan
        scp -i $SSH_KEY -r "AI-solver-reviewer\backend" "${EC2_USER}@${EC2_HOST}:~/ai-reviewer-backend/"
        
        Write-Host "`nBackend deployed! Now SSH into EC2 and run:" -ForegroundColor Green
        Write-Host "cd ~/ai-reviewer-backend" -ForegroundColor Yellow
        Write-Host "pip install -r requirements.txt" -ForegroundColor Yellow
        Write-Host "python run.py" -ForegroundColor Yellow
    }
    "2" {
        Write-Host "`nDeploying Simple Frontend..." -ForegroundColor Cyan
        scp -i $SSH_KEY -r "AI-solver-reviewer\frontend-simple" "${EC2_USER}@${EC2_HOST}:~/ai-reviewer-frontend/"
        
        Write-Host "`nFrontend deployed! Now SSH into EC2 and run:" -ForegroundColor Green
        Write-Host "cd ~/ai-reviewer-frontend" -ForegroundColor Yellow
        Write-Host "python3 -m http.server 8080" -ForegroundColor Yellow
        Write-Host "`nOr set up Nginx (see README.md)" -ForegroundColor Yellow
    }
    "3" {
        Write-Host "`nDeploying both Backend and Frontend..." -ForegroundColor Cyan
        scp -i $SSH_KEY -r "AI-solver-reviewer\backend" "${EC2_USER}@${EC2_HOST}:~/ai-reviewer-backend/"
        scp -i $SSH_KEY -r "AI-solver-reviewer\frontend-simple" "${EC2_USER}@${EC2_HOST}:~/ai-reviewer-frontend/"
        
        Write-Host "`nBoth deployed! Now SSH into EC2 and run:" -ForegroundColor Green
        Write-Host "`nIn one terminal:" -ForegroundColor Yellow
        Write-Host "cd ~/ai-reviewer-backend" -ForegroundColor Yellow
        Write-Host "pip install -r requirements.txt" -ForegroundColor Yellow
        Write-Host "python run.py" -ForegroundColor Yellow
        Write-Host "`nIn another terminal:" -ForegroundColor Yellow
        Write-Host "cd ~/ai-reviewer-frontend" -ForegroundColor Yellow
        Write-Host "python3 -m http.server 8080" -ForegroundColor Yellow
    }
    default {
        Write-Host "Invalid choice. Exiting." -ForegroundColor Red
        exit 1
    }
}

Write-Host "`nWould you like to SSH into the EC2 instance now? (y/n)" -ForegroundColor Green
$sshChoice = Read-Host

if ($sshChoice -eq "y" -or $sshChoice -eq "Y") {
    Write-Host "`nConnecting to EC2..." -ForegroundColor Cyan
    ssh -i $SSH_KEY "${EC2_USER}@${EC2_HOST}"
}

Write-Host "`nDeployment complete!" -ForegroundColor Green
