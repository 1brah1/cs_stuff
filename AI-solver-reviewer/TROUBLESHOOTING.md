# Troubleshooting Guide

## Python Issues

### "Python was not found"

**Solution:** Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation
- See `PYTHON_SETUP.md` for detailed instructions

### "Module not found" or "No module named 'fastapi'"

**Solution:** Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### "pip is not recognized"

**Solution:** 
- Reinstall Python and check "Add Python to PATH"
- Or add Python Scripts folder to PATH manually

## Database Issues

### "Connection refused" or "Could not connect to database"

**Solutions:**
1. Make sure PostgreSQL is running
2. Check `DATABASE_URL` in `backend/.env` is correct
3. Verify database exists: `CREATE DATABASE ai_reviewer_db;`
4. See `DATABASE_SETUP.md` for detailed setup

### "Database does not exist"

**Solution:** Create the database
```sql
CREATE DATABASE ai_reviewer_db;
```

## Backend Issues

### "Port 8000 already in use"

**Solution:** Change port in `backend/run.py`
```python
uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
```

### Backend starts but shows errors

**Check:**
1. Database connection string in `.env`
2. All dependencies installed: `pip install -r requirements.txt`
3. PostgreSQL service is running

## Frontend Issues

### "npm is not recognized"

**Solution:** Install Node.js from https://nodejs.org/

### "Cannot connect to backend"

**Solutions:**
1. Make sure backend is running on `http://localhost:8000`
2. Check `REACT_APP_API_URL` in `frontend/.env`
3. Check CORS settings in backend

### "Module not found" in frontend

**Solution:** Install dependencies
```bash
cd frontend
npm install
```

## General Setup Checklist

- [ ] Python 3.11+ installed and in PATH
- [ ] Node.js 18+ installed
- [ ] PostgreSQL installed and running
- [ ] Database `ai_reviewer_db` created
- [ ] `backend/.env` file exists with correct DATABASE_URL
- [ ] `frontend/.env` file exists with REACT_APP_API_URL
- [ ] Backend dependencies installed: `pip install -r requirements.txt`
- [ ] Frontend dependencies installed: `npm install`

## Getting Help

If you're stuck:
1. Check the specific error message
2. Look in the relevant setup guide (PYTHON_SETUP.md, DATABASE_SETUP.md)
3. Verify all prerequisites are installed
4. Check that services (PostgreSQL) are running





