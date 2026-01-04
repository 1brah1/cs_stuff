# Quick Database Setup

PostgreSQL is installed at: `C:\Program Files\PostgreSQL\13\bin\psql.exe`

## Option 1: Using PowerShell Script (Easiest)

Run this command with your PostgreSQL password:

```powershell
cd C:\Users\ibrah\CODE\cs_stuff\AI-solver-reviewer
.\create_db_with_password.ps1 -Password "your_postgres_password"
```

Replace `your_postgres_password` with your actual PostgreSQL password.

## Option 2: Using pgAdmin (GUI - Recommended)

1. **Open pgAdmin** from Start Menu
2. **Connect to your PostgreSQL server:**
   - Enter your PostgreSQL password when prompted
3. **Create the database:**
   - Right-click on "Databases" → "Create" → "Database"
   - Name: `ai_reviewer_db`
   - Click "Save"
4. **Update backend/.env:**
   - Open `backend/.env`
   - Update this line:
     ```
     DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ai_reviewer_db
     ```
   - Replace `YOUR_PASSWORD` with your PostgreSQL password

## Option 3: Using psql Command Line

1. **Open PowerShell**
2. **Set your password:**
   ```powershell
   $env:PGPASSWORD = "your_postgres_password"
   ```
3. **Create the database:**
   ```powershell
   & "C:\Program Files\PostgreSQL\13\bin\psql.exe" -U postgres -h localhost -p 5432 -d postgres -c "CREATE DATABASE ai_reviewer_db;"
   ```
4. **Update backend/.env** (same as Option 2)

## Verify Database Created

After creating, verify it exists:

```powershell
$env:PGPASSWORD = "your_password"
& "C:\Program Files\PostgreSQL\13\bin\psql.exe" -U postgres -h localhost -p 5432 -d postgres -c "\l" | Select-String "ai_reviewer_db"
```

You should see `ai_reviewer_db` in the list.

## Update .env File

After creating the database, make sure `backend/.env` has the correct connection string:

```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ai_reviewer_db
```

Replace `YOUR_PASSWORD` with your actual PostgreSQL password.

## Test Connection

Once the database is created and .env is updated, test the backend:

```bash
# In Anaconda Prompt
conda activate ai-reviewer
cd backend
python run.py
```

If the database connection works, the server will start successfully!

## Common Issues

### "password authentication failed"
- Make sure you're using the correct PostgreSQL password
- Check if PostgreSQL service is running

### "database does not exist"
- Make sure you created the database with the exact name: `ai_reviewer_db`
- Check spelling in DATABASE_URL

### "connection refused"
- Make sure PostgreSQL service is running
- Check if port 5432 is correct
- Verify host is `localhost`

