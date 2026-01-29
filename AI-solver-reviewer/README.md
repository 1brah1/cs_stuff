# AI Document Reviewer

AI-powered document review application using DeepSeek R1 via OpenRouter API. Upload documents and get instant AI feedback on content quality, grammar, structure, and improvements.

🌐 **Live Demo:** http://13.211.53.117:8000/docs

---

## 🎯 What It Does

1. **Upload** - Drop a .txt or .pdf file
2. **Review** - AI analyzes your document in seconds
3. **Improve** - Get actionable feedback on quality, grammar, and structure

---

## 🏗️ Architecture

```
┌─────────────┐      HTTP      ┌─────────────┐      API      ┌──────────────┐
│   React     │ ────────────▶  │   FastAPI   │ ───────────▶  │  OpenRouter  │
│  Frontend   │                │   Backend   │               │  (DeepSeek)  │
└─────────────┘                └─────────────┘               └──────────────┘
                                      │
                                      ▼
                                ┌──────────┐
                                │  SQLite  │
                                └──────────┘
```

### Tech Stack

**Backend:**
- FastAPI (Python web framework)
- SQLite (document storage)
- OpenRouter API (AI integration)
- Session-based data management (1-hour expiration)

**Frontend:**
- React 18 + TypeScript
- Glassmorphism UI design
- Drag-and-drop file upload

**Deployment:**
- Backend: AWS EC2 + Docker
- Frontend: GitHub Pages

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenRouter API key ([get one here](https://openrouter.ai/))

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
python setup_env.py
# Enter your OpenRouter API key when prompted

# Run server
python run.py
```

Backend runs at `http://localhost:8000`  
API docs at `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure API endpoint
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start development server
npm start
```

Frontend runs at `http://localhost:3000`

---

## 📦 How It Works

### 1. Session Management
- Each user gets a unique session ID (stored in browser)
- Documents expire after 1 hour
- Background cleanup runs every 15 minutes

### 2. Document Upload
```
User uploads file → Extract text → Store in SQLite → Return document ID
```

### 3. AI Review
```
Request review → Send to DeepSeek R1 → Parse response → Store review → Return to user
```

### 4. Data Flow
```python
# Backend endpoint
POST /api/v1/documents/upload
  ↓
Document stored with session_id + expires_at
  ↓
POST /api/v1/reviews/{document_id}
  ↓
OpenRouter API call → DeepSeek R1 analysis
  ↓
Review stored and returned
```

---

## 🔐 Environment Variables

### Backend `.env`
```env
DATABASE_URL=sqlite:///./data/ai_reviewer.db
OPENROUTER_API_KEY=sk-or-v1-your-key-here
JWT_SECRET_KEY=your-secret-key
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

### Frontend `.env`
```env
REACT_APP_API_URL=http://localhost:8000
```

---

## 🚢 Deployment

### Deploy Backend to EC2

```powershell
# From project root
.\deploy.ps1 -EC2_IP "YOUR_IP" -KeyFile "path\to\key.pem" -OpenRouterKey "YOUR_KEY"
```

This script:
1. Copies backend files to EC2
2. Creates production `.env`
3. Builds and starts Docker containers
4. Tests health endpoint

### Deploy Frontend to GitHub Pages

```bash
# Automatic via GitHub Actions
git push origin main

# Or manual
cd frontend
npm run build
# Copy build to _site and push to gh-pages branch
```

---

## 📁 Project Structure

```
AI-solver-reviewer/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # API routes
│   │   ├── core/                # Config & session
│   │   ├── db/                  # Database setup
│   │   ├── models/              # SQLAlchemy models
│   │   └── services/            # OpenRouter integration
│   ├── requirements.txt
│   ├── run.py
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Upload, Review, History
│   │   └── services/            # API client
│   ├── package.json
│   └── Dockerfile
├── docker-compose.prod.yml      # Production deployment
├── deploy.ps1                   # Deployment script
└── README.md
```

---

## 🔧 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Get access token

### Documents
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents` - List documents (paginated)
- `GET /api/v1/documents/{id}` - Get document details

### Reviews
- `POST /api/v1/reviews/{document_id}` - Generate AI review
- `GET /api/v1/reviews/{document_id}` - Get document reviews
- `GET /api/v1/reviews` - List all reviews (paginated)

**Headers Required:**
- `Authorization: Bearer {token}`
- `X-Session-Id: {uuid}`

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Verify environment
cat backend/.env
```

### Frontend can't connect
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app/main.py`
- Verify `REACT_APP_API_URL` in frontend `.env`

### Upload fails on GitHub Pages
- GitHub Pages (HTTPS) can't call HTTP backend
- **Solution:** Run frontend locally with `npm start`

### Database issues
```bash
# Reset database
rm backend/data/ai_reviewer.db
python backend/run.py  # Recreates tables
```

---

## 🔒 Security Features

- ✅ Session-based isolation (users only see their documents)
- ✅ Automatic data expiration (1-hour TTL)
- ✅ JWT authentication
- ✅ CORS protection
- ✅ No credentials in code (environment variables only)

---

## 📊 Database Schema

```sql
-- Documents table
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    filename VARCHAR NOT NULL,
    file_type VARCHAR NOT NULL,
    content TEXT NOT NULL,
    session_id VARCHAR NOT NULL,
    expires_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Reviews table
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

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

---

## 📝 License

MIT License - see [LICENSE](./LICENSE) file.

---

## 👤 Author

**Ibrahim**
- GitHub: [@1brah1](https://github.com/1brah1)
- Portfolio: https://1brah1.github.io/cs_stuff/

---

## 🙏 Acknowledgments

- [OpenRouter](https://openrouter.ai/) - AI API gateway
- [DeepSeek](https://www.deepseek.com/) - R1 language model
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library

---

**Last Updated:** January 2025
