# Quick Start Guide

Get the AI Document Reviewer up and running in 5 minutes!

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (local or use Render)
- OpenRouter API key (already in setup script)

## 1. Backend Setup (2 minutes)

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (includes API keys)
python setup_env.py

# Update DATABASE_URL in .env if needed
# For local: DATABASE_URL=postgresql://user:password@localhost:5432/ai_reviewer_db

# Start backend
python run.py
```

Backend running at `http://localhost:8000`

## 2. Frontend Setup (2 minutes)

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start frontend
npm start
```

Frontend running at `http://localhost:3000`

## 3. Test It Out! (1 minute)

1. Open `http://localhost:3000`
2. Upload a `.txt` or `.pdf` file
3. Click "Generate New Review"
4. View the AI-generated feedback!

## API Keys

Already configured in `backend/setup_env.py`:
- OpenRouter API Key: `Your own API Key`

## Troubleshooting

**Backend won't start?**
- Check PostgreSQL is running
- Verify DATABASE_URL in `.env`
- Check port 8000 is free

**Frontend can't connect?**
- Verify backend is running
- Check REACT_APP_API_URL in frontend/.env
- Check browser console for errors

**Database errors?**
- Create database: `createdb ai_reviewer_db`
- Update DATABASE_URL with correct credentials

## Next Steps

- See [SETUP.md](./SETUP.md) for detailed setup
- See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment
- See [README.md](./README.md) for full documentation


