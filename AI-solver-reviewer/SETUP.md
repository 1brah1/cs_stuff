# Quick Setup Guide

## Initial Setup

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (run the setup script)
python setup_env.py

# Or create .env manually with:
# DATABASE_URL=postgresql://user:password@localhost:5432/ai_reviewer_db
# OPENROUTER_API_KEY=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
# JWT_SECRET_KEY=your-secret-key-change-in-production
# JWT_ALGORITHM=HS256
# FRONTEND_URL=http://localhost:3000
# ENVIRONMENT=development

# Set up PostgreSQL database (if not already set up)
# Create database: createdb ai_reviewer_db

# Run the backend
python run.py
```

Backend will run on `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start development server
npm start
```

Frontend will run on `http://localhost:3000`

## API Keys

The following API keys are already configured in the setup script:

- **OpenRouter API Key**: `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`
- **Render API Key**: `rnd_QmKAIRotV8XIz89oiuLYBsvQ8xFT`

**Security Note**: In production, store these as environment variables or secrets, never commit them to version control.

## Database Setup

### Local Development

1. Install PostgreSQL if not already installed
2. Create database:
   ```bash
   createdb ai_reviewer_db
   ```
3. Update `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=postgresql://your_username:your_password@localhost:5432/ai_reviewer_db
   ```

### Production (Render)

1. Create PostgreSQL database on Render
2. Use the Internal Database URL provided by Render
3. Set `DATABASE_URL` environment variable in Render dashboard

## Testing the Application

1. Start backend: `cd backend && python run.py`
2. Start frontend: `cd frontend && npm start`
3. Open browser: `http://localhost:3000`
4. Upload a document (.txt or .pdf)
5. Generate a review
6. View review history

## Troubleshooting

### Backend won't start
- Check PostgreSQL is running
- Verify DATABASE_URL in .env is correct
- Check port 8000 is not in use

### Frontend can't connect to backend
- Verify backend is running on port 8000
- Check REACT_APP_API_URL in frontend/.env
- Check CORS settings in backend

### Database connection errors
- Verify PostgreSQL is installed and running
- Check database exists
- Verify credentials in DATABASE_URL

## Next Steps

- See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment instructions
- See [README.md](./README.md) for full documentation

