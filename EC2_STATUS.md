# ✅ EC2 Deployment Complete!

## Services Running

### Backend API
- **URL:** http://13.211.53.117:8000
- **Status:** ✅ Running (PID: 6300)
- **API Docs:** http://13.211.53.117:8000/docs
- **Process:** uvicorn app.main:app --host 0.0.0.0 --port 8000

### Frontend Application  
- **URL:** http://13.211.53.117:8080
- **Status:** ✅ Running (PID: 126290)
- **Process:** python3 -m http.server 8080
- **Location:** ~/ai-reviewer/frontend-simple

---

## How to Access

1. **Live Application:** http://13.211.53.117:8080
2. **API Documentation:** http://13.211.53.117:8000/docs
3. **Backend Health:** http://13.211.53.117:8000/health

---

## Managing Services

### Check Status
```bash
ssh -i "C:\Users\ibrah\OneDrive\Documents\Gaylord.pem" ubuntu@13.211.53.117
ps aux | grep python
```

### View Logs
```bash
# Backend logs (if using run.py)
tail -f ~/ai-reviewer/backend/nohup.out

# Frontend logs
tail -f ~/frontend.log
```

### Restart Services

**Restart Frontend:**
```bash
# Kill existing
pkill -f "http.server 8080"

# Start new
cd ~/ai-reviewer/frontend-simple
nohup python3 -m http.server 8080 > ~/frontend.log 2>&1 &
```

**Restart Backend:**
```bash
# Kill existing
pkill -f uvicorn

# Start new
cd ~/ai-reviewer/backend
source venv/bin/activate
python run.py
```

---

## Services Are Running in Background

Both services are now running in background (using `nohup`), so they will continue even after you disconnect from SSH.

To make them start automatically on boot, you would need to create systemd service files (optional).

---

## Next Steps

1. ✅ Push portfolio to GitHub: `git push origin main`
2. ✅ Test the live application: http://13.211.53.117:8080
3. ✅ Upload a document and chat with AI
4. ✅ Verify session cleanup works

---

## Troubleshooting

**If frontend doesn't respond:**
```bash
ssh -i "C:\Users\ibrah\OneDrive\Documents\Gaylord.pem" ubuntu@13.211.53.117
cd ~/ai-reviewer/frontend-simple
nohup python3 -m http.server 8080 > ~/frontend.log 2>&1 &
```

**If backend doesn't respond:**
```bash
# Check if it's running
ps aux | grep uvicorn

# If not, restart it
cd ~/ai-reviewer/backend
source venv/bin/activate  
python run.py
```
