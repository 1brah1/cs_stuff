# Deployment Guide

This guide provides step-by-step instructions for deploying the AI Document Reviewer application.

## Prerequisites

- GitHub account with repository access
- Render account (for backend)
- OpenRouter API key
- Render API key (optional, for CLI deployment)

## Backend Deployment (Render)

### Step 1: Create PostgreSQL Database on Render

1. Log in to [Render](https://render.com)
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `ai-reviewer-db`
   - **Database**: `ai_reviewer_db`
   - **User**: `ai_reviewer_user`
   - **Region**: Choose closest to your users
   - **Plan**: Free tier (for demo) or paid (for production)
4. Click "Create Database"
5. Copy the **Internal Database URL** (you'll need this later)

### Step 2: Create Web Service for Backend

1. In Render dashboard, click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select the repository and branch (usually `main`)
4. Configure the service:
   - **Name**: `ai-reviewer-backend`
   - **Environment**: `Python 3`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"

### Step 3: Configure Environment Variables

In the Render dashboard for your web service, go to "Environment" and add:

- `DATABASE_URL`: Internal Database URL from Step 1
- `OPENROUTER_API_KEY`: `sk-or-v1-YOUR_API_KEY_HERE`
- `JWT_SECRET_KEY`: Generate a random secret (e.g., `openssl rand -hex 32`)
- `FRONTEND_URL`: Your GitHub Pages URL (e.g., `https://yourusername.github.io/ai-solver-reviewer`)
- `ENVIRONMENT`: `production`

### Step 4: Deploy

1. Render will automatically deploy on the first setup
2. Wait for deployment to complete (usually 2-5 minutes)
3. Copy your service URL (e.g., `https://ai-reviewer-backend.onrender.com`)

### Step 5: Test Backend

Visit: `https://your-backend-url.onrender.com/health`

Should return: `{"status": "healthy"}`

## Frontend Deployment (GitHub Pages)

### Step 1: Enable GitHub Pages

1. Go to your GitHub repository
2. Click "Settings" → "Pages"
3. Under "Source", select:
   - **Branch**: `gh-pages` (will be created automatically)
   - **Folder**: `/ (root)` or `/frontend/build` depending on workflow
4. Click "Save"

### Step 2: Configure GitHub Secrets

1. Go to repository "Settings" → "Secrets and variables" → "Actions"
2. Add the following secrets:
   - `REACT_APP_API_URL`: Your Render backend URL (e.g., `https://ai-reviewer-backend.onrender.com`)
   - `OPENROUTER_API_KEY`: Your OpenRouter API key (for reference)
   - `RENDER_API_KEY`: Your Render API key (optional, for automated deployments)

### Step 3: Update Workflow (if needed)

The `deploy-frontend.yml` workflow should already be configured. Verify:
- It builds from `frontend/` directory
- Uses `REACT_APP_API_URL` secret
- Deploys to GitHub Pages

### Step 4: Trigger Deployment

1. Push to `main` branch (workflow runs automatically)
2. Or manually trigger: "Actions" → "Deploy Frontend to GitHub Pages" → "Run workflow"

### Step 5: Verify Deployment

1. Wait for workflow to complete (~5 minutes)
2. Visit your GitHub Pages URL: `https://yourusername.github.io/ai-solver-reviewer`
3. Test document upload and review features

## Database Setup

### Initial Schema Creation

The application automatically creates database tables on first run. If you need to manually set up:

1. Connect to your Render PostgreSQL database
2. Tables will be created automatically when the backend starts
3. For migrations, use Alembic (already included):

```bash
cd backend
alembic upgrade head
```

## CORS Configuration

Ensure your backend `FRONTEND_URL` matches your GitHub Pages URL exactly (including `https://`).

## Environment Variables Reference

### Backend (Render)
```
DATABASE_URL=postgresql://user:password@hostname:5432/dbname
OPENROUTER_API_KEY=sk-or-v1-...
JWT_SECRET_KEY=your-secret-key
FRONTEND_URL=https://yourusername.github.io/ai-solver-reviewer
ENVIRONMENT=production
```

### Frontend (GitHub Secrets)
```
REACT_APP_API_URL=https://your-backend.onrender.com
```

## Troubleshooting

### Backend Issues

**Database Connection Failed**
- Verify `DATABASE_URL` uses internal URL on Render
- Check database is running
- Verify credentials are correct

**OpenRouter API Errors**
- Verify API key is correct
- Check API key has credits/quota
- Review backend logs in Render dashboard

**CORS Errors**
- Ensure `FRONTEND_URL` matches GitHub Pages URL exactly
- Check backend logs for CORS errors
- Verify CORS middleware is configured correctly

### Frontend Issues

**Build Fails**
- Check Node.js version (should be 18+)
- Verify all dependencies in `package.json`
- Review build logs in GitHub Actions

**API Connection Failed**
- Verify `REACT_APP_API_URL` secret is set correctly
- Check backend is running and accessible
- Test backend URL directly in browser
- Check browser console for CORS errors

**GitHub Pages Not Updating**
- Verify workflow completed successfully
- Check "Pages" settings in repository
- Clear browser cache
- Wait a few minutes for DNS propagation

## Monitoring

### Backend Logs (Render)
- View logs in Render dashboard
- Check for errors, warnings
- Monitor API response times

### Frontend (GitHub Actions)
- View workflow logs in "Actions" tab
- Check build and deployment status
- Review any error messages

## Production Checklist

- [ ] Database is using production plan (not free tier)
- [ ] Environment variables are set correctly
- [ ] CORS is configured for production frontend URL
- [ ] JWT secret is strong and secure
- [ ] API keys are stored as secrets (not in code)
- [ ] HTTPS is enabled (automatic on Render)
- [ ] GitHub Pages uses HTTPS (automatic)
- [ ] Database backups are configured (Render)
- [ ] Monitoring is set up (optional)
- [ ] Error tracking is configured (optional)

## Support

For deployment issues:
1. Check Render dashboard logs
2. Review GitHub Actions workflow logs
3. Verify all environment variables
4. Test API endpoints directly
5. Check browser console for frontend errors





