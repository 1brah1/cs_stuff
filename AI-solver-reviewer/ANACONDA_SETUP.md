# Anaconda Setup Guide

## Using Anaconda for This Project

Anaconda includes Python and makes it easy to manage environments. Here's how to set it up:

## Option 1: Use Anaconda Prompt (Easiest)

1. **Open Anaconda Prompt** from Start Menu
   - Search for "Anaconda Prompt" or "Anaconda PowerShell Prompt"

2. **Navigate to project:**
   ```bash
   cd C:\Users\ibrah\CODE\cs_stuff\AI-solver-reviewer\backend
   ```

3. **Create conda environment:**
   ```bash
   conda create -n ai-reviewer python=3.11 -y
   ```

4. **Activate environment:**
   ```bash
   conda activate ai-reviewer
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the backend:**
   ```bash
   python run.py
   ```

## Option 2: Initialize Anaconda in PowerShell

If you want to use conda in regular PowerShell:

1. **Find Anaconda installation:**
   - Usually at: `C:\Users\YourName\Anaconda3\`
   - Or: `C:\ProgramData\Anaconda3\`

2. **Initialize conda:**
   ```powershell
   & "C:\Users\YourName\Anaconda3\Scripts\Anaconda3-64.exe" -Command "conda init powershell"
   ```

3. **Restart PowerShell** and then use conda commands

4. **Create and activate environment:**
   ```powershell
   conda create -n ai-reviewer python=3.11 -y
   conda activate ai-reviewer
   cd backend
   pip install -r requirements.txt
   python run.py
   ```

## Option 3: Use Setup Script

Run the automated setup script:

```powershell
.\setup_conda.ps1
```

This will find Anaconda and create the environment for you.

## Quick Commands Reference

**Create environment:**
```bash
conda create -n ai-reviewer python=3.11 -y
```

**Activate environment:**
```bash
conda activate ai-reviewer
```

**Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

**Run backend:**
```bash
python run.py
```

**Deactivate environment (when done):**
```bash
conda deactivate
```

## Using the Environment

Every time you want to work on this project:

1. Open **Anaconda Prompt**
2. Run: `conda activate ai-reviewer`
3. Navigate to: `cd C:\Users\ibrah\CODE\cs_stuff\AI-solver-reviewer\backend`
4. Run: `python run.py`

## Troubleshooting

### "conda is not recognized"

**Solution:** Use Anaconda Prompt instead of regular PowerShell/CMD
- Or initialize conda in your current shell (see Option 2)

### "Environment already exists"

**Solution:** Either:
- Use existing: `conda activate ai-reviewer`
- Remove and recreate: `conda remove -n ai-reviewer --all -y` then create again

### "Module not found" errors

**Solution:** Make sure environment is activated and dependencies are installed:
```bash
conda activate ai-reviewer
pip install -r requirements.txt
```

## Why Use Conda Environment?

- Isolates project dependencies
- Easy to manage Python versions
- Can be shared/recreated easily
- Prevents conflicts with other projects

## Next Steps

After setting up the conda environment:

1. ✅ Environment created
2. ✅ Dependencies installed
3. ⏭️ Set up database (see `DATABASE_SETUP.md`)
4. ⏭️ Start backend: `python run.py`
5. ⏭️ Start frontend: `cd ../frontend && npm start`

