# Deployment Guide

Production hosting is **Render** (backend) + **GitHub Pages** (frontend). AWS EC2 is no longer used.

**Live URLs**

- Frontend: [https://1brah1.github.io/cs_stuff/ai-reviewer/](https://1brah1.github.io/cs_stuff/ai-reviewer/)
- API: [https://cs-stuff-1.onrender.com](https://cs-stuff-1.onrender.com)
- API docs: [https://cs-stuff-1.onrender.com/docs](https://cs-stuff-1.onrender.com/docs)

The Render free tier sleeps after about 15 minutes idle. The first request after that can take 30–60 seconds.

---

## 1. Backend (Render)

Service dashboard: [https://dashboard.render.com/web/srv-daa7at95efls73dufi30](https://dashboard.render.com/web/srv-daa7at95efls73dufi30)

### Create or update the web service

1. [Render Dashboard](https://dashboard.render.com) → **New** → **Web Service**
2. Connect repo `1brah1/cs_stuff`
3. Settings:

| Setting | Value |
|---------|-------|
| Branch | `main` |
| Root Directory | `AI-solver-reviewer/backend` |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Plan | Free |

`runtime.txt` pins Python **3.12.7**. Without this, Render may pick Python 3.14 and the `pydantic==2.5.0` install will fail.

### Environment variables

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.12.7` |
| `OPENROUTER_API_KEY` | From [openrouter.ai/keys](https://openrouter.ai/keys) |
| `JWT_SECRET_KEY` | Random string (`openssl rand -hex 32`) |
| `DATABASE_URL` | `sqlite:///./data/ai_reviewer.db` |
| `FRONTEND_URL` | `https://1brah1.github.io` |
| `ENVIRONMENT` | `production` |

Do **not** commit `backend/.env`. Secrets belong in the Render dashboard only.

### Redeploy

Push to `main`. Render rebuilds from `AI-solver-reviewer/backend`.

```bash
git push origin main
```

Or use **Manual Deploy** in the Render dashboard.

### Verify

- [https://cs-stuff-1.onrender.com/health](https://cs-stuff-1.onrender.com/health) → `{"status":"healthy"}`
- [https://cs-stuff-1.onrender.com/docs](https://cs-stuff-1.onrender.com/docs) → Swagger UI

---

## 2. Frontend (GitHub Pages)

GitHub Pages is served from the **`gh-pages`** branch (not `main`).

```bash
cd AI-solver-reviewer/frontend
# .env.production already sets REACT_APP_API_URL=https://cs-stuff-1.onrender.com
npm install
npm run build
```

Copy `frontend/build/` onto `gh-pages` as `ai-reviewer/`, then push:

```bash
git checkout gh-pages
# replace ai-reviewer/ with the new build output
git add ai-reviewer
git commit -m "Point AI reviewer frontend at Render API"
git push origin gh-pages
```

**Verify**

- Portfolio: [https://1brah1.github.io/cs_stuff/](https://1brah1.github.io/cs_stuff/)
- AI Reviewer: [https://1brah1.github.io/cs_stuff/ai-reviewer/](https://1brah1.github.io/cs_stuff/ai-reviewer/)

Leave the existing **stock-analysis-api** Render service on `gh-pages` alone (`srv-d8dsn3po3t8c73esgrdg`).

---

## 3. Branch map

| What | Branch | Path |
|------|--------|------|
| AI reviewer backend | `main` | `AI-solver-reviewer/backend/` |
| AI reviewer frontend source | `main` | `AI-solver-reviewer/frontend/` |
| Published static site | `gh-pages` | `ai-reviewer/` |
| Stock API | `gh-pages` | `stock_analysis_portfolio/` |

---

## Troubleshooting

### Build fails with `pydantic-core` / `maturin`

Render used Python 3.14. Set `PYTHON_VERSION=3.12.7` and keep `runtime.txt`.

### First page load is slow

Free-tier cold start. Wait and retry.

### Upload works but review fails

Check `OPENROUTER_API_KEY` on the Render service.

### Mixed content / CORS

The API is HTTPS. The frontend origin is `https://1brah1.github.io`. Backend CORS currently allows all origins.

### SQLite data disappeared

Expected on Render redeploy. Fine for a portfolio demo.

---

## Checklist

Before deploy:

- [ ] `OPENROUTER_API_KEY` set on Render
- [ ] `PYTHON_VERSION=3.12.7`
- [ ] `FRONTEND_URL=https://1brah1.github.io`

After deploy:

- [ ] `/health` returns healthy
- [ ] `/docs` loads
- [ ] GitHub Pages app loads
- [ ] Upload a `.txt` file and generate a review

---

## Need help?

See [README.md](./README.md) for local setup and API details.
