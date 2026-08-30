# AWS EC2 Setup Guide for AI-Solver-Reviewer

> **Deprecated.** Production hosting moved to Render + GitHub Pages. See [DEPLOYMENT.md](./DEPLOYMENT.md). This file is kept only as a historical AWS reference.

## Prerequisites
- AWS Account (Account ID: 250025622892)
- AWS CLI installed and configured
- SSH key pair for EC2 access

## Step 1: Create EC2 Instance

### Using AWS Console

1. **Navigate to EC2 Dashboard**
   - Go to AWS Console → EC2

2. **Launch Instance**
   - Click "Launch Instance"
   - Name: `ai-reviewer-backend`
   
3. **AMI Selection**
   - Choose: **Ubuntu Server 22.04 LTS** (free tier eligible)
   
4. **Instance Type**
   - Select: **t2.small** or **t3.small** (recommended)
   - Note: t2.micro may be insufficient for Docker + PostgreSQL

5. **Key Pair**
   - Create new key pair: `ai-reviewer-key.pem`
   - Download and save securely
   - Set permissions: `chmod 400 ai-reviewer-key.pem`

6. **Network Settings**
   - Create security group: `ai-reviewer-sg`
   - Allow inbound rules:
     - SSH (22) from Your IP
     - HTTP (80) from Anywhere  
     - HTTPS (443) from Anywhere
     - Custom TCP (8000) from Anywhere (for FastAPI)

7. **Storage**
   - 20 GB gp3 (minimum)
   - 30 GB recommended

8. **Launch Instance**

## Step 2: Connect to EC2 Instance

```bash
ssh -i "ai-reviewer-key.pem" ubuntu@<EC2-PUBLIC-IP>
```

## Step 3: Install Docker and Docker Compose

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installations
docker --version
docker-compose --version

# Log out and back in for group changes to take effect
exit
```

## Step 4: Prepare Application Directory

```bash
# Reconnect to EC2
ssh -i "ai-reviewer-key.pem" ubuntu@<EC2-PUBLIC-IP>

# Create application directory
mkdir -p ~/ai-reviewer
cd ~/ai-reviewer
```

## Step 5: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and Variables → Actions

Add the following secrets:

1. **EC2_HOST**
   - Value: Your EC2 public IP or DNS (e.g., `52.23.45.67`)

2. **EC2_USERNAME**
   - Value: `ubuntu` (for Ubuntu AMI) or `ec2-user` (for Amazon Linux)

3. **EC2_SSH_KEY**
   - Value: Contents of your `ai-reviewer-key.pem` file
   ```bash
   cat ai-reviewer-key.pem  # Copy entire output
   ```

4. ** OPENROUTER_API_KEY**
   - Value: Your OpenRouter API key (starts with `sk-or-v1-...`)

5. **JWT_SECRET_KEY**
   - Value: Generate a secure random string
   ```bash
   openssl rand -hex 32
   ```

## Step 6: Initial Deployment

### Option A: Manual Deployment (First Time)

1. Copy files to EC2:
```bash
# From your local machine
scp -i "ai-reviewer-key.pem" -r backend docker-compose.prod.yml ubuntu@<EC2-PUBLIC-IP>:~/ai-reviewer/
```

2. SSH into EC2 and deploy:
```bash
ssh -i "ai-reviewer-key.pem" ubuntu@<EC2-PUBLIC-IP>

cd ~/ai-reviewer

# Create .env file
cat > .env << EOF
OPENROUTER_API_KEY=sk-or-v1-your-key-here
JWT_SECRET_KEY=your-generated-secret-here
GITHUB_USERNAME=your-github-username
EOF

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Option B: Automated Deployment via GitHub Actions

1. Push your code to main branch
2. GitHub Actions will automatically deploy
3. Monitor deployment in Actions tab

## Step 7: Verify Deployment

1. **Check Health Endpoint**
   ```bash
   curl http://<EC2-PUBLIC-IP>:8000/health
   ```
   
   Expected response:
   ```json
   {"status":"healthy"}
   ```

2. **Check API Docs**
   - Visit: `http://<EC2-PUBLIC-IP>:8000/docs`

3. **Test Document Upload**
   - Use the frontend or Postman to test uploads

## Step 8: Set Up Domain (Optional)

1. **Register Domain** (e.g., AWS Route 53, Namecheap)

2. **Create A Record**
   - Point to EC2 Public IP

3. **Install SSL Certificate**
   ```bash
   # Install Certbot
   sudo snap install --classic certbot
   
   # Obtain certificate
   sudo certbot --nginx -d your-domain.com
   ```

## Step 9: Configure Automatic Startups

```bash
# Ensure Docker starts on boot
sudo systemctl enable docker

# Create systemd service for app (optional)
sudo tee /etc/systemd/system/ai-reviewer.service > /dev/null <<EOF
[Unit]
Description=AI Reviewer Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/ai-reviewer
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml down
User=ubuntu

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable ai-reviewer
sudo systemctl start ai-reviewer
```

## Maintenance Commands

### View Logs
```bash
cd ~/ai-reviewer
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f postgres
```

### Restart Services
```bash
docker-compose -f docker-compose.prod.yml restart
```

### Update Application
```bash
git pull origin main  # If using git on EC2
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

### Database Backup
```bash
docker exec ai-reviewer-postgres pg_dump -U postgres ai_reviewer_db > backup_$(date +%Y%m%d).sql
```

### Clean Up
```bash
# Remove old images
docker image prune -f

# Remove stopped containers
docker container prune -f
```

## Monitoring

### Check Resource Usage
```bash
# Docker stats
docker stats

# System resources
htop
df -h
```

### Set Up CloudWatch (Optional)
- Install CloudWatch agent on EC2
- Monitor CPU, memory, and disk usage
- Set up alarms for high resource usage

##Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Check database connection
docker exec -it ai-reviewer-backend env | grep DATABASE_URL
```

### Database connection errors
```bash
# Verify PostgreSQL is running
docker ps | grep postgres

# Test connection
docker exec -it ai-reviewer-postgres psql -U postgres -d ai_reviewer_db
```

### Port 8000 not accessible
```bash
# Check security group allows inbound on port 8000
# Check if service is listening
sudo netstat -tlnp | grep 8000
```

## Security Best Practices

1. **Never expose sensitive keys in code**
2. **Use EC2 IAM roles** instead of static credentials where possible
3. **Implement rate limiting** in production
4. **Regular updates**: `sudo apt update && sudo apt upgrade`
5. **Monitor logs** for suspicious activity
6. **Use HTTPS** in production with valid SSL certificate

## Cost Optimization

-**Use t3.small** for better price/performance
- **Enable detailed monitoring** to track usage
- **Stop instance** when not needed (development)
- **Use Reserved Instances** for production (save up to 60%)

---

**Need Help?**
- Check GitHub Actions logs for deployment errors
- Review backend logs for application errors
- Consult AWS documentation for infrastructure issues
