#!/bin/bash
# Deploy to EC2 - Run this FROM your local machine

# Configuration - UPDATE THESE VALUES
EC2_IP="13.211.53.117"
EC2_USER="ubuntu"
KEY_FILE="Gaylord.pem"
OPENROUTER_KEY="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"
JWT_SECRET=$(openssl rand -hex 32 2>/dev/null || echo "change-this-secret-key-in-production")

echo "🚀 Deploying AI-Reviewer to EC2..."

# Copy files to EC2
echo "📤 Copying files to EC2..."
scp -i "$KEY_FILE" -r backend docker-compose.prod.yml $EC2_USER@$EC2_IP:~/ai-reviewer/

# Deploy on EC2
echo "🔧 Setting up and starting services..."
ssh -i "$KEY_FILE" $EC2_USER@$EC2_IP << EOF
cd ~/ai-reviewer

# Create .env file
cat > .env << ENVEOF
OPENROUTER_API_KEY=$OPENROUTER_KEY
JWT_SECRET_KEY=$JWT_SECRET
GITHUB_USERNAME=$(git config user.name || echo "your-username")
ENVEOF

# Start services
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
docker-compose -f docker-compose.prod.yml up -d

echo ""
echo "✅ Deployment complete!"
echo "🌐 Backend: http://$EC2_IP:8000"
echo "📚 API Docs: http://$EC2_IP:8000/docs"
EOF

echo ""
echo "✅ Deployment finished!"
echo "🔍 Testing health endpoint..."
sleep 5
curl -s http://$EC2_IP:8000/health || echo "⚠️  Service starting... wait 30s and try: curl http://$EC2_IP:8000/health"
