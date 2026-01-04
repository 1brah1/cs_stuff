# Docker Setup Guide

## Using Docker for Frontend

Since Node.js isn't installed locally, we can use Docker to run the frontend instead!

## Quick Start

### Option 1: Use Docker Compose (Easiest)

```bash
# From project root
docker-compose up frontend
```

### Option 2: Use the Setup Script

**Windows PowerShell:**
```powershell
.\run_frontend_docker.ps1
```

**Linux/Mac:**
```bash
chmod +x run_frontend_docker.sh
./run_frontend_docker.sh
```

### Option 3: Manual Docker Commands

1. **Pull Node.js image:**
   ```bash
   docker pull node:24-alpine
   ```

2. **Build frontend image:**
   ```bash
   cd frontend
   docker build -t ai-reviewer-frontend .
   ```

3. **Run the container:**
   ```bash
   docker run -it --rm \
     -p 3000:3000 \
     -v "$(pwd):/app" \
     -v "/app/node_modules" \
     -e REACT_APP_API_URL=http://localhost:8000 \
     ai-reviewer-frontend
   ```

## Complete Setup Workflow

### Terminal 1: Backend (Anaconda Prompt)

```bash
conda activate ai-reviewer
cd C:\Users\ibrah\CODE\cs_stuff\AI-solver-reviewer\backend
pip install -r requirements.txt
python run.py
```

Backend runs on: `http://localhost:8000`

### Terminal 2: Frontend (Docker)

**Option A - Docker Compose:**
```bash
cd C:\Users\ibrah\CODE\cs_stuff\AI-solver-reviewer
docker-compose up frontend
```

**Option B - PowerShell Script:**
```powershell
cd C:\Users\ibrah\CODE\cs_stuff\AI-solver-reviewer
.\run_frontend_docker.ps1
```

**Option C - Manual Docker:**
```bash
cd frontend
docker build -t ai-reviewer-frontend .
docker run -it --rm -p 3000:3000 -v "${PWD}:/app" -v "/app/node_modules" -e REACT_APP_API_URL=http://localhost:8000 ai-reviewer-frontend
```

Frontend runs on: `http://localhost:3000`

## First Time Setup

1. **Make sure Docker Desktop is running**
   - Start Docker Desktop application
   - Wait for it to fully start (whale icon in system tray)

2. **Pull Node.js image (if not already done):**
   ```bash
   docker pull node:24-alpine
   ```

3. **Build the frontend image:**
   ```bash
   cd frontend
   docker build -t ai-reviewer-frontend .
   ```

## Docker Commands Reference

**Build image:**
```bash
docker build -t ai-reviewer-frontend ./frontend
```

**Run container:**
```bash
docker run -it --rm -p 3000:3000 ai-reviewer-frontend
```

**Stop container:**
- Press `Ctrl+C` in the terminal running the container

**View running containers:**
```bash
docker ps
```

**Stop a specific container:**
```bash
docker stop <container-id>
```

## Troubleshooting

### "Docker is not running"
- Start Docker Desktop application
- Wait for it to fully initialize
- Check system tray for Docker icon

### "Port 3000 already in use"
- Stop any other services using port 3000
- Or change the port mapping: `-p 3001:3000`

### "Cannot connect to backend"
- Make sure backend is running on `http://localhost:8000`
- Check `REACT_APP_API_URL` environment variable
- Verify CORS settings in backend

### "Module not found" errors
- Rebuild the Docker image: `docker build -t ai-reviewer-frontend ./frontend`
- Make sure `package.json` is in the frontend directory

## Development Workflow

1. **Start Docker Desktop**
2. **Terminal 1 - Backend (Anaconda):**
   ```bash
   conda activate ai-reviewer
   cd backend
   python run.py
   ```
3. **Terminal 2 - Frontend (Docker):**
   ```bash
   docker-compose up frontend
   # or
   .\run_frontend_docker.ps1
   ```
4. **Open browser:** `http://localhost:3000`

## Benefits of Using Docker

- ✅ No need to install Node.js locally
- ✅ Consistent environment across machines
- ✅ Easy to share and deploy
- ✅ Isolated from system dependencies
- ✅ Easy to clean up (just remove container)

## Next Steps

Once both services are running:
1. Backend: `http://localhost:8000`
2. Frontend: `http://localhost:3000`
3. Test the application by uploading a document!

