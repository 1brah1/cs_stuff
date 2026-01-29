# EC2 Deployment Guide

## Backend Setup

### Prerequisites
- EC2 instance running Ubuntu
- SSH access with key file
- Python 3.8+ installed

### Deployment Steps

1. **SSH into EC2:**
```bash
ssh -i "path/to/your-key.pem" ubuntu@<YOUR_EC2_IP>
```

2. **Update system:**
```bash
sudo apt update
sudo apt upgrade -y
```

3. **Install Python dependencies:**
```bash
sudo apt install python3-pip python3-venv -y
```

4. **Create application directory:**
```bash
mkdir -p ~/ai-reviewer
cd ~/ai-reviewer
```

5. **Copy backend files** (from your local machine in PowerShell):
```powershell
scp -i "path/to/your-key.pem" -r AI-solver-reviewer\backend ubuntu@<YOUR_EC2_IP>:~/ai-reviewer/
```

6. **Set up Python environment** (on EC2):
```bash
cd ~/ai-reviewer/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

7. **Create .env file:**
```bash
nano .env
```

Add this content:
```
DATABASE_URL=sqlite:///./data/ai_reviewer.db
OPENROUTER_API_KEY=your_api_key_here
FRONTEND_URL=http://<YOUR_EC2_IP>:8080
ENVIRONMENT=production
```

Press Ctrl+X, then Y, then Enter to save.

8. **Create data directory:**
```bash
mkdir -p data
mkdir -p uploads
```

9. **Run the backend:**
```bash
python run.py
```

The backend will start on `http://0.0.0.0:8000`

### Keep Backend Running (tmux)

To keep the backend running after you disconnect:

1. **Install tmux:**
```bash
sudo apt install tmux -y
```

2. **Start a tmux session:**
```bash
tmux new -s ai-backend
```

3. **Run the backend:**
```bash
cd ~/ai-reviewer/backend
source venv/bin/activate
python run.py
```

4. **Detach from tmux:**
Press `Ctrl+B`, then `D`

5. **Reattach later:**
```bash
tmux attach -t ai-backend
```

---

## Frontend Setup (Simple HTML)

### Option 1: Python HTTP Server (Quick & Easy)

1. **Copy frontend files** (from local PowerShell):
```powershell
scp -i "C:\Users\ibrah\OneDrive\Documents\Gaylord.pem" -r AI-solver-reviewer\frontend-simple ubuntu@13.211.53.117:~/ai-reviewer/
```

2. **On EC2, start server:**
```bash
cd ~/ai-reviewer/frontend-simple
python3 -m http.server 8080
```

Access at: `http://13.211.53.117:8080`

### Option 2: Nginx (Recommended for Production)

1. **Install Nginx:**
```bash
sudo apt install nginx -y
```

2. **Copy frontend files:**
```bash
sudo mkdir -p /var/www/ai-reviewer
sudo cp -r ~/ai-reviewer/frontend-simple/* /var/www/ai-reviewer/
```

3. **Create Nginx config:**
```bash
sudo nano /etc/nginx/sites-available/ai-reviewer
```

Add this content:
```nginx
server {
    listen 80;
    server_name 13.211.53.117;

    root /var/www/ai-reviewer;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to backend
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

4. **Enable the site:**
```bash
sudo ln -s /etc/nginx/sites-available/ai-reviewer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

Access at: `http://13.211.53.117`

---

## EC2 Security Group Settings

Make sure your EC2 security group allows:
- Port 22 (SSH)
- Port 80 (HTTP for Nginx)
- Port 8000 (Backend API)
- Port 8080 (Python HTTP Server, if using Option 1)

---

## Testing

1. **Test backend:**
```bash
curl http://13.211.53.117:8000/health
```

2. **Test API docs:**
Open: `http://13.211.53.117:8000/docs`

3. **Test frontend:**
- Python Server: `http://13.211.53.117:8080`
- Nginx: `http://13.211.53.117`

---

## Troubleshooting

### Backend not accessible
```bash
# Check if backend is running
ps aux | grep python

# Check backend logs
cd ~/ai-reviewer/backend
cat nohup.out  # if using nohup
```

### Port already in use
```bash
# Find process using port 8000
sudo lsof -i :8000
# Kill it if needed
sudo kill -9 <PID>
```

### Nginx issues
```bash
# Check Nginx status
sudo systemctl status nginx

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

---

## Quick Start Script

Save this to `~/start-ai-reviewer.sh`:
```bash
#!/bin/bash
cd ~/ai-reviewer/backend
source venv/bin/activate
python run.py
```

Make executable and run:
```bash
chmod +x ~/start-ai-reviewer.sh
~/start-ai-reviewer.sh
```
