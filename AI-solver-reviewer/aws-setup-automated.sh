#!/bin/bash
# Automated EC2 Setup Script - Run this ON your EC2 instance after connecting

set -e

echo "🚀 Starting AI-Reviewer EC2 Setup..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
rm get-docker.sh

# Install Docker Compose
echo "🔧 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create app directory
echo "📁 Creating application directory..."
mkdir -p ~/ai-reviewer
cd ~/ai-reviewer

# Enable Docker on boot
sudo systemctl enable docker

echo "✅ Setup complete!"
echo ""
echo "⚠️  IMPORTANT: Log out and back in for Docker permissions to take effect"
echo "   Run: exit"
echo "   Then reconnect: ssh -i your-key.pem ubuntu@your-ec2-ip"
echo ""
echo "📋 Next steps:"
echo "   1. Copy your project files to ~/ai-reviewer/"
echo "   2. Create .env file with your secrets"
echo "   3. Run: docker-compose -f docker-compose.prod.yml up -d"
