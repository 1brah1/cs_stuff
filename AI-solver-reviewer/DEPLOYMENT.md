# Deployment Guide

## 🚀 Quick Deployment Steps

### 1. Deploy Backend to EC2

**From your local machine (PowerShell):**

```powershell
cd AI-solver-reviewer
.\deploy.ps1 -EC2_IP "<YOUR_EC2_IP>" -KeyFile "..\<YOUR_KEY_FILE>.pem" -OpenRouterKey "YOUR_API_KEY_HERE"
```

This will:
- Copy backend files to EC2
- Create .env with your secrets
- Build and start Docker containers
- Test the deployment

**Verify:**
- Health: http://13.211.53.117:8000/health
- API Docs: http://13.211.53.117:8000/docs

---

### 2. Deploy Frontend to GitHub Pages

**Option A: Automatic (Recommended)**

Just push to GitHub:
```bash
git add .
git commit -m "Deploy updates"
git push origin main
```

GitHub Actions will automatically build and deploy.

**Option B: Manual**

```bash
cd AI-solver-reviewer/frontend
npm run build
cd ../..
mkdir _site
copy index.html _site\
xcopy /E /I AI-solver-reviewer\frontend\build _site\ai-reviewer
cd _site
git init
git add -A
git commit -m "Deploy"
git branch -M gh-pages
git remote add origin https://github.com/1brah1/cs_stuff.git
git push -f origin gh-pages
```

**Verify:**
- Portfolio: https://1brah1.github.io/cs_stuff/
- AI Reviewer: https://1brah1.github.io/cs_stuff/ai-reviewer/

---

## 📋 GitHub Secrets Required

Go to: https://github.com/1brah1/cs_stuff/settings/secrets/actions

Add these secrets:

| Secret Name | Value | How to Get |
|------------|-------|------------|
| `OPENROUTER_API_KEY` | Your API key | https://openrouter.ai/ |
| `JWT_SECRET_KEY` | Random 32-char hex | Run: `openssl rand -hex 32` |
| `EC2_HOST` | `13.211.53.117` | Your EC2 public IP |
| `EC2_USERNAME` | `ubuntu` | EC2 username |
| `EC2_SSH_KEY` | Contents of <YOUR_KEY_FILE>.pem | Copy entire file |

---

## 🔄 Update Deployment

**Backend:**
```powershell
cd AI-solver-reviewer
.\deploy.ps1 -EC2_IP "<YOUR_EC2_IP>" -KeyFile "..\<YOUR_KEY_FILE>.pem" -OpenRouterKey "YOUR_KEY"
```

**Frontend:**
```bash
git push origin main
```

---

## 🐛 Troubleshooting

### Backend not starting
```bash
ssh -i <YOUR_KEY_FILE>.pem ubuntu@<YOUR_EC2_IP>
cd ~/ai-reviewer
docker-compose -f docker-compose.prod.yml logs backend
```

### Frontend upload fails
**Issue:** HTTPS/HTTP mixed content  
**Solution:** Run locally for now:
```bash
cd AI-solver-reviewer/frontend
npm start
```
Visit: http://localhost:3000

### Database reset
```bash
ssh -i <YOUR_KEY_FILE>.pem ubuntu@<YOUR_EC2_IP>
cd ~/ai-reviewer/backend
rm -rf data/
docker-compose -f docker-compose.prod.yml restart
```

---

## ✅ Checklist

Before deploying:
- [ ] GitHub secrets configured
- [ ] EC2 security group allows port 8000
- [ ] Docker installed on EC2
- [ ] OpenRouter API key obtained
- [ ] .pem key file has correct permissions

After deploying:
- [ ] Backend health check passes
- [ ] API docs accessible
- [ ] Frontend loads on GitHub Pages
- [ ] Can upload documents locally

---

## 📞 Need Help?

Check the main README.md for detailed troubleshooting.
