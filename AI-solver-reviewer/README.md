# AI Document Reviewer

AI-powered document review application using DeepSeek via OpenRouter. Upload a `.txt` or `.pdf` file and get instant feedback on content quality, grammar, structure, and improvements.

**Live demo:** [https://1brah1.github.io/cs_stuff/ai-reviewer/](https://1brah1.github.io/cs_stuff/ai-reviewer/)  
**API docs:** [https://cs-stuff-1.onrender.com/docs](https://cs-stuff-1.onrender.com/docs)

The Render free tier sleeps after about 15 minutes of idle time. The first request after that can take 30–60 seconds to wake up.

---

## What it does

1. **Upload** — drop a `.txt` or `.pdf` file
2. **Review** — the AI analyzes the document
3. **Improve** — get actionable feedback on quality, grammar, and structure

---

## Architecture

```
┌─────────────┐      HTTPS     ┌─────────────┐      API      ┌──────────────┐
│ GitHub Pages│ ────────────▶  │   Render    │ ───────────▶  │  OpenRouter  │
│  React SPA  │                │  FastAPI    │               │  (DeepSeek)  │
└─────────────┘                └─────────────┘               └──────────────┘
                                      │
                                      ▼
                                ┌──────────┐
                                │  SQLite  │
                                └──────────┘
```

### Tech stack

**Backend**
- FastAPI
- SQLite (document storage; resets on Render redeploy)
- OpenRouter API
- Session-based data with 1-hour expiration

**Frontend**
- React 18 + TypeScript
- Drag-and-drop file upload

**Deployment**
- Backend: Render free web service (`https://cs-stuff-1.onrender.com`)
- Frontend: GitHub Pages (`gh-pages` branch)

---

## Quick start

### Prerequisites

- Python 3.12+
- Node.js 18+
- OpenRouter API key ([get one here](https://openrouter.ai/))

### Backend

```bash
cd backend

pip install -r requirements.txt
python setup_env.py
python run.py
```

Backend: `http://localhost:8000`  
API docs: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend

npm install
echo "REACT_APP_API_URL=http://localhost:8000" > .env
npm start
```

Frontend: `http://localhost:3000`

---

## How it works

### Session management

- Each visitor gets a session ID stored in the browser
- Documents expire after 1 hour
- Background cleanup runs every 15 minutes

### Document upload

```
User uploads file → Extract text → Store in SQLite → Return document ID
```

### AI review

```
Request review → Send to DeepSeek → Store review → Return to user
```

### Data flow

```
POST /api/v1/auth/login
POST /api/v1/documents/upload   (X-Session-Id header)
POST /api/v1/reviews/{document_id}
```

---

## Environment variables

### Backend `.env`

```env
DATABASE_URL=sqlite:///./data/ai_reviewer.db
OPENROUTER_API_KEY=sk-or-v1-your-key-here
JWT_SECRET_KEY=your-secret-key
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

On Render, set the same keys in the dashboard. Also set `PYTHON_VERSION=3.12.7`.

### Frontend `.env` / `.env.production`

```env
REACT_APP_API_URL=http://localhost:8000
```

Production build uses `https://cs-stuff-1.onrender.com`.

---

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for the full Render + GitHub Pages steps.

**Backend:** push to `main` (root directory `AI-solver-reviewer/backend`). Render redeploys automatically.

**Frontend:** build with `REACT_APP_API_URL=https://cs-stuff-1.onrender.com`, copy the `build/` output into `ai-reviewer/` on the `gh-pages` branch, and push.

---

## Project structure

```
AI-solver-reviewer/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # API routes (auth, documents, reviews, chat)
│   │   ├── core/                # Config and session
│   │   ├── db/                  # Database setup
│   │   ├── models/              # SQLAlchemy models
│   │   └── services/            # OpenRouter integration
│   ├── requirements.txt
│   ├── runtime.txt              # Python 3.12.7 for Render
│   ├── run.py
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/               # Upload, Review, History
│   │   └── services/            # API client
│   └── package.json
└── README.md
```

---

## API endpoints

### Authentication

- `POST /api/v1/auth/login` — demo token (`demo_user` / `demo`)

### Documents

- `POST /api/v1/documents/upload` — upload document
- `GET /api/v1/documents` — list documents
- `GET /api/v1/documents/{id}` — get document details

### Reviews

- `POST /api/v1/reviews/{document_id}` — generate AI review
- `GET /api/v1/reviews/{document_id}` — get document reviews
- `GET /api/v1/reviews` — list reviews

**Headers:** `X-Session-Id: {uuid}` (required for upload and list). Optional `Authorization: Bearer {token}`.

---

## Troubleshooting

### Backend will not start locally

```bash
cat backend/.env
python backend/run.py
```

### Frontend cannot connect

- Confirm the API is running
- Check CORS in `backend/app/main.py`
- Verify `REACT_APP_API_URL` (rebuild after changing it)

### First request on the live site is slow

Render free tier cold start. Wait 30–60 seconds and retry.

### Upload fails

- Confirm `OPENROUTER_API_KEY` is set on Render (needed for reviews, not upload)
- Confirm `X-Session-Id` is sent (the frontend sets this automatically)
- SQLite data on Render resets on each redeploy

### Database reset (local)

```bash
rm backend/data/ai_reviewer.db
python backend/run.py
```

---

## Security

- Session isolation (users only see their own documents)
- Automatic 1-hour expiration
- Demo JWT login for the portfolio UI
- CORS enabled
- Secrets live in environment variables, not in source

---

## Database schema

```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    filename VARCHAR NOT NULL,
    file_type VARCHAR NOT NULL,
    content TEXT NOT NULL,
    session_id VARCHAR NOT NULL,
    expires_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id),
    review_text TEXT NOT NULL,
    status VARCHAR DEFAULT 'completed',
    expires_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## License

MIT License — see [LICENSE](./LICENSE).

---

## Author

**Ibrahim**  
GitHub: [@1brah1](https://github.com/1brah1)  
Portfolio: [https://1brah1.github.io/cs_stuff/](https://1brah1.github.io/cs_stuff/)

---

## Acknowledgments

- [OpenRouter](https://openrouter.ai/) — AI API gateway
- [DeepSeek](https://www.deepseek.com/) — language model
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [Render](https://render.com/) — backend hosting

---

**Last updated:** August 2026
