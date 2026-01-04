# How to Start the Application

## Quick Start

You now have everything set up! Here's how to run the application:

## Terminal 1: Backend (Anaconda Prompt)

```bash
conda activate ai-reviewer
cd C:\Users\ibrah\CODE\cs_stuff\AI-solver-reviewer\backend
python run.py
```

**Backend will run on:** `http://localhost:8000`

## Terminal 2: Frontend (Docker)

You have 3 options:

### Option 1: Docker Compose (Recommended)
```bash
cd C:\Users\ibrah\CODE\cs_stuff\AI-solver-reviewer
docker-compose up frontend
```

### Option 2: PowerShell Script
```powershell
cd C:\Users\ibrah\CODE\cs_stuff\AI-solver-reviewer
.\run_frontend_docker.ps1
```

### Option 3: Manual Docker Command
```bash
cd C:\Users\ibrah\CODE\cs_stuff\AI-solver-reviewer\frontend
docker run -it --rm -p 3000:3000 -v "${PWD}:/app" -v "/app/node_modules" -e REACT_APP_API_URL=http://localhost:8000 ai-reviewer-frontend
```

**Frontend will run on:** `http://localhost:3000`

## Complete Workflow

1. **Start Docker Desktop** (if not already running)

2. **Terminal 1 - Start Backend:**
   - Open **Anaconda Prompt**
   - Run:
     ```bash
     conda activate ai-reviewer
     cd C:\Users\ibrah\CODE\cs_stuff\AI-solver-reviewer\backend
     python run.py
     ```
   - Wait for: `Uvicorn running on http://0.0.0.0:8000`

3. **Terminal 2 - Start Frontend:**
   - Open **PowerShell** or **CMD**
   - Run:
     ```bash
     cd C:\Users\ibrah\CODE\cs_stuff\AI-solver-reviewer
     docker-compose up frontend
     ```
   - Wait for: `webpack compiled successfully`

4. **Open Browser:**
   - Go to: `http://localhost:3000`
   - You should see the AI Document Reviewer interface!

## Test the Application

1. **Upload a document:**
   - Click "Upload" or drag and drop a `.txt` or `.pdf` file
   - Wait for upload to complete

2. **Generate a review:**
   - Click "Generate New Review"
   - Wait for AI to analyze the document
   - View the detailed feedback!

3. **View history:**
   - Click "History" in the navigation
   - See all your uploaded documents

## Troubleshooting

### Backend won't start
- Make sure conda environment is activated
- Check if dependencies are installed: `pip install -r requirements.txt`
- Verify database is set up (see `DATABASE_SETUP.md`)

### Frontend won't start
- Make sure Docker Desktop is running
- Check if image is built: `docker images | grep ai-reviewer-frontend`
- Rebuild if needed: `docker build -t ai-reviewer-frontend ./frontend`

### Can't connect to backend
- Verify backend is running on port 8000
- Check `REACT_APP_API_URL` in frontend Docker container
- Test backend directly: `http://localhost:8000/health`

### Port already in use
- Backend: Change port in `backend/run.py`
- Frontend: Change port mapping in `docker-compose.yml` (e.g., `3001:3000`)

## What's Running

- ✅ **Backend:** FastAPI server on port 8000
- ✅ **Frontend:** React app on port 3000
- ✅ **Database:** PostgreSQL (needs to be set up - see `DATABASE_SETUP.md`)

## Next Steps

1. **Set up PostgreSQL database** (if not done):
   - See `DATABASE_SETUP.md`
   - Create database: `ai_reviewer_db`
   - Update `DATABASE_URL` in `backend/.env`

2. **Test the full workflow:**
   - Upload document
   - Generate review
   - View history

3. **Ready for development!**
   - Backend code: `backend/app/`
   - Frontend code: `frontend/src/`
   - Make changes and see them hot-reload!

## Stop the Application

- **Backend:** Press `Ctrl+C` in Terminal 1
- **Frontend:** Press `Ctrl+C` in Terminal 2 (or `docker-compose down`)

Enjoy your AI Document Reviewer! 🚀

