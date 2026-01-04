# PostgreSQL Database Setup Guide

## Quick Setup (Automated)

Run the setup script:
```powershell
.\setup_database.ps1
```

The script will:
1. Find your PostgreSQL installation
2. Ask for your database credentials
3. Create the `ai_reviewer_db` database
4. Update `backend/.env` with the connection string

## Manual Setup

If the script doesn't work, follow these steps:

### Step 1: Find PostgreSQL Installation

PostgreSQL is usually installed in one of these locations:
- `C:\Program Files\PostgreSQL\16\bin\`
- `C:\Program Files\PostgreSQL\15\bin\`
- `C:\Program Files\PostgreSQL\14\bin\`

### Step 2: Add PostgreSQL to PATH (Optional but Recommended)

1. Open System Properties → Environment Variables
2. Edit "Path" in System variables
3. Add: `C:\Program Files\PostgreSQL\16\bin` (or your version)
4. Click OK and restart your terminal

### Step 3: Create Database

**Option A: Using psql command line**

Open a new terminal and run:
```bash
# Navigate to PostgreSQL bin directory
cd "C:\Program Files\PostgreSQL\16\bin"

# Connect to PostgreSQL (you'll be prompted for password)
psql -U postgres

# In psql, run:
CREATE DATABASE ai_reviewer_db;

# Exit psql
\q
```

**Option B: Using pgAdmin (GUI)**

1. Open pgAdmin (usually in Start Menu)
2. Connect to your PostgreSQL server
3. Right-click on "Databases" → "Create" → "Database"
4. Name: `ai_reviewer_db`
5. Click "Save"

**Option C: Using SQL Command**

If you can access psql, run:
```sql
CREATE DATABASE ai_reviewer_db;
```

### Step 4: Update backend/.env

Edit `backend/.env` and update the DATABASE_URL:

```
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/ai_reviewer_db
```

Replace:
- `your_username` - Your PostgreSQL username (usually `postgres`)
- `your_password` - Your PostgreSQL password
- `localhost` - Database host (use `localhost` for local)
- `5432` - Database port (default is 5432)
- `ai_reviewer_db` - Database name (we just created this)

**Example:**
```
DATABASE_URL=postgresql://postgres:mypassword@localhost:5432/ai_reviewer_db
```

### Step 5: Test Connection

You can test if the connection works by starting the backend:

```bash
cd backend
python run.py
```

If the database connection is successful, the server will start. If there's an error, check:
- Database name is correct
- Username and password are correct
- PostgreSQL service is running
- Port number is correct

## Common Issues

### "psql is not recognized"
- PostgreSQL bin directory is not in PATH
- Use full path: `"C:\Program Files\PostgreSQL\16\bin\psql.exe"`
- Or add it to PATH (see Step 2 above)

### "Password authentication failed"
- Check your PostgreSQL password
- Default user is usually `postgres`
- You may need to reset the password in pgAdmin

### "Database already exists"
- The database was already created
- You can skip the CREATE DATABASE step
- Just update the .env file

### "Connection refused"
- PostgreSQL service might not be running
- Start it from Services (services.msc) or pgAdmin
- Check if port 5432 is correct

## Verify Setup

After setup, verify everything works:

1. **Check database exists:**
   ```bash
   psql -U postgres -l
   ```
   You should see `ai_reviewer_db` in the list

2. **Test backend connection:**
   ```bash
   cd backend
   python run.py
   ```
   Should start without database errors

3. **Check API:**
   - Open: http://localhost:8000/health
   - Should return: `{"status": "healthy"}`

## Next Steps

Once the database is set up:
1. Install backend dependencies: `cd backend && pip install -r requirements.txt`
2. Start backend: `cd backend && python run.py`
3. Install frontend dependencies: `cd frontend && npm install`
4. Start frontend: `cd frontend && npm start`

