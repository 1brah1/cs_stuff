# Python Setup Guide

## Issue: Python Not Found

If you're getting "Python was not found", you need to install Python or add it to your PATH.

## Solution 1: Install Python (Recommended)

1. **Download Python:**
   - Go to https://www.python.org/downloads/
   - Download Python 3.11 or newer (Windows installer)

2. **Install Python:**
   - Run the installer
   - **IMPORTANT:** Check the box "Add Python to PATH" at the bottom of the installer
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation:**
   - Close and reopen your terminal
   - Run: `python --version`
   - Should show: `Python 3.11.x` or similar

4. **Install Dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

5. **Run the Backend:**
   ```bash
   python run.py
   ```

## Solution 2: Use Python Launcher (if already installed)

If Python is installed but not in PATH, try:

```bash
# Try py launcher
py run.py

# Or python3
python3 run.py

# Or find Python and use full path
# Usually: C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe
```

## Solution 3: Find Existing Python Installation

If Python might already be installed:

1. **Check common locations:**
   - `C:\Python39\`
   - `C:\Python310\`
   - `C:\Python311\`
   - `C:\Users\YourName\AppData\Local\Programs\Python\`

2. **Add to PATH:**
   - Open System Properties → Environment Variables
   - Edit "Path" in System variables
   - Add the Python installation folder (e.g., `C:\Python311`)
   - Add the Scripts folder (e.g., `C:\Python311\Scripts`)
   - Click OK and restart terminal

## Solution 4: Use Virtual Environment (if Python is installed)

If Python is installed but dependencies aren't:

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt

# Run the backend
python run.py
```

## Quick Test

After installing Python, test it:

```bash
python --version
pip --version
```

Both should work without errors.

## Common Issues

### "Execution Policy" Error in PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "pip is not recognized"
- Make sure you checked "Add Python to PATH" during installation
- Or add Python Scripts folder to PATH manually

### "Module not found" errors
- Install dependencies: `pip install -r requirements.txt`
- Make sure you're in the `backend` directory

## Next Steps After Python Works

1. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up database** (if not done):
   - See `DATABASE_SETUP.md`

3. **Start backend:**
   ```bash
   python run.py
   ```

4. **In another terminal, start frontend:**
   ```bash
   cd frontend
   npm install
   npm start
   ```

