# Setup Status

## Completed Steps

✅ Environment files created:
- `backend/.env` - Backend environment configuration (includes OpenRouter API key)
- `frontend/.env` - Frontend environment configuration

## Next Steps to Complete Setup

### 1. Backend Setup

**Install Python dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

If you don't have Python installed, download it from https://www.python.org/downloads/

**Update Database URL:**
Edit `backend/.env` and update the `DATABASE_URL` with your PostgreSQL connection string:
```
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/ai_reviewer_db
```

If you don't have PostgreSQL installed:
- Download from https://www.postgresql.org/download/
- Or use Docker: `docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres`
- Create database: `createdb ai_reviewer_db`

**Start the backend:**
```bash
cd backend
python run.py
```

The backend will run on `http://localhost:8000`

### 2. Frontend Setup

**Install Node.js dependencies:**
```bash
cd frontend
npm install
```

If you don't have Node.js installed, download it from https://nodejs.org/

**Start the frontend:**
```bash
cd frontend
npm start
```

The frontend will run on `http://localhost:3000`

## Quick Start Commands

Once dependencies are installed, you can start both services:

**Terminal 1 (Backend):**
```bash
cd backend
python run.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm start
```

## Verification

1. Backend should be accessible at: http://localhost:8000
2. API docs available at: http://localhost:8000/docs
3. Frontend should open automatically at: http://localhost:3000
4. Try uploading a document and generating a review!

## Troubleshooting

**Python not found:**
- Install Python 3.11+ from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

**Node.js not found:**
- Install Node.js 18+ from https://nodejs.org/

**Database connection errors:**
- Make sure PostgreSQL is running
- Verify DATABASE_URL in backend/.env is correct
- Create the database: `createdb ai_reviewer_db`

**Port already in use:**
- Backend uses port 8000, change it in `run.py` if needed
- Frontend uses port 3000, it will prompt to use a different port if needed

## Configuration Files Created

- `backend/.env` - Contains OpenRouter API key and database configuration
- `frontend/.env` - Contains backend API URL

Both files are configured for local development. Update them as needed for your environment.


