# Deployment Summary

## What's Ready to Deploy

### 1. GitHub Pages (Static Portfolio)
✅ **Ready to deploy automatically via Git push**

**Files:**
- `index.html` - Main portfolio page
- `stock-portfolio.html` - Stock analysis showcase  
- `ai-reviewer/` - AI reviewer showcase page
- `bluetooth_robot_car/website/` - Robot car page
- `stock_analysis_portfolio/visualizations/` - Stock charts

**Deploy:**
```powershell
cd C:\Users\ibrah\CODE\cs_stuff
git add .
git commit -m "Update portfolio with fixes and AI reviewer"
git push origin main
```

GitHub Actions will automatically deploy to `https://1brah1.github.io/cs_stuff/`

### 2. EC2 Backend (AI Document Reviewer API)
⚠️ **Requires manual deployment**

**What you need:**
- OpenRouter API Key: `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`
- EC2 Host: `13.211.53.117`
- SSH Key: `C:\Users\ibrah\OneDrive\Documents\Gaylord.pem`

**Deploy Backend:**
```powershell
# From Windows PowerShell
scp -i "C:\Users\ibrah\OneDrive\Documents\Gaylord.pem" -r AI-solver-reviewer\backend ubuntu@13.211.53.117:~/ai-reviewer/
```

**Then on EC2:**
```bash
ssh -i "C:\Users\ibrah\OneDrive\Documents\Gaylord.pem" ubuntu@13.211.53.117

cd ~/ai-reviewer/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=sqlite:///./data/ai_reviewer.db
OPENROUTER_API_KEY=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
JWT_SECRET_KEY=production-secret-key-change-this
JWT_ALGORITHM=HS256
FRONTEND_URL=*
ENVIRONMENT=production
EOF

# Create directories
mkdir -p data uploads

# Run backend
python run.py
```

Backend will be available at: `http://13.211.53.117:8000`
API Docs at: `http://13.211.53.117:8000/docs`

### 3. EC2 Frontend (AI Document Reviewer App)
⚠️ **Requires manual deployment**

**Deploy Frontend:**
```powershell
# From Windows PowerShell
scp -i "C:\Users\ibrah\OneDrive\Documents\Gaylord.pem" -r AI-solver-reviewer\frontend-simple ubuntu@13.211.53.117:~/ai-reviewer/
```

**Then on EC2 (in a new terminal/tmux session):**
```bash
cd ~/ai-reviewer/frontend-simple
python3 -m http.server 8080
```

Frontend will be available at: `http://13.211.53.117:8080`

## Keep Services Running with tmux

To keep services running after you disconnect:

**Install tmux:**
```bash
sudo apt install tmux -y
```

**Start backend in tmux:**
```bash
tmux new -s backend
cd ~/ai-reviewer/backend
source venv/bin/activate
python run.py
# Press Ctrl+B then D to detach
```

**Start frontend in tmux:**
```bash
tmux new -s frontend
cd ~/ai-reviewer/frontend-simple
python3 -m http.server 8080
# Press Ctrl+B then D to detach
```

**Reattach to sessions:**
```bash
tmux attach -t backend
tmux attach -t frontend
```

## Files Excluded from Git

These files won't be committed (already in .gitignore):
- ✅ `tasks.md` - Your original task file
- ✅ `Answers.md` - Your answers file
- ✅ `*.ps1` - PowerShell scripts (like deploy-ai-reviewer.ps1)
- ✅ `.env` files - Environment variables with secrets
- ✅ `*.db` - Database files
- ✅ `uploads/` - User uploaded files

## What Happens After Git Push

1. GitHub Actions workflow runs
2. Copies static HTML files to `_site/` directory
3. Deploys to GitHub Pages
4. Your portfolio updates at `https://1brah1.github.io/cs_stuff/`

**Timeline:** Usually takes 1-2 minutes

## URLs After Deployment

### GitHub Pages (Automatic)
- Main Portfolio: `https://1brah1.github.io/cs_stuff/`
- Stock Analysis: `https://1brah1.github.io/cs_stuff/stock-portfolio.html`
- Robot Car: `https://1brah1.github.io/cs_stuff/bluetooth_robot_car/website/`
- AI Reviewer Showcase: `https://1brah1.github.io/cs_stuff/ai-reviewer/`

### EC2 (Manual - After you deploy)
- Frontend App: `http://13.211.53.117:8080`
- Backend API: `http://13.211.53.117:8000`
- API Documentation: `http://13.211.53.117:8000/docs`

## Testing Checklist

After deployment, verify:

### GitHub Pages
- [ ] Main page loads without emojis
- [ ] Stock portfolio shows all 6 images
- [ ] All GitHub links work  
- [ ] AI reviewer showcase loads
- [ ] "Launch Application" button links to EC2

### EC2
- [ ] Backend responds at port 8000
- [ ] Frontend loads at port 8080
- [ ] Can upload PDF files
- [ ] Can upload TXT files
- [ ] AI chat works
- [ ] Session cleanup on browser close

## Next Steps

1. **Push to GitHub** to deploy static pages
2. **Deploy to EC2** following the commands above
3. **Test everything** using the checklist
4. **Keep tmux sessions running** so services stay up
