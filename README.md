## Quick Start

### AI Document Reviewer

**EC2 Deployment (Manual):**

See [EC2_DEPLOYMENT.md](EC2_DEPLOYMENT.md) for detailed instructions.

Quick version:
```bash
# 1. Copy backend files to EC2
scp -i <path/to/key.pem> -r AI-solver-reviewer\backend ubuntu@<YOUR_EC2_IP>:~/ai-reviewer/

# 2. Copy frontend files to EC2
scp -i <path/to/key.pem> -r AI-solver-reviewer\frontend-simple ubuntu@<YOUR_EC2_IP>:~/ai-reviewer/

# 3. SSH into EC2
ssh -i <path/to/key.pem> ubuntu@<YOUR_EC2_IP>

# 4. Install dependencies and run backend
cd ~/ai-reviewer/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Create .env with OPENROUTER_API_KEY
nohup python run.py > backend.log 2>&1 &

# 5. In another terminal, run frontend
cd ~/ai-reviewer/frontend-simple
nohup python3 -m http.server 8080 > frontend.log 2>&1 &
```

---

## Repository Structure

```
cs_stuff/
├── .github/
│   └── workflows/             # GitHub Actions
│       └── deploy-frontend.yml  # GitHub Pages deployment
├── AI-solver-reviewer/         # AI Document Reviewer
│   ├── backend/              # FastAPI backend
│   ├── frontend-simple/      # Simple HTML/CSS/JS frontend (EC2)
│   └── frontend/             # React frontend (legacy, not used)
├── stock_analysis_portfolio/  # Stock analysis
├── bluetooth_robot_car/      # Robot car project
├── ai-reviewer/              # GitHub Pages showcase for AI reviewer
├── index.html                # Main portfolio page
├── stock-portfolio.html      # Stock portfolio page
└── EC2_DEPLOYMENT.md         # EC2 deployment guide
```

---

## 🛠️ Technologies Used

### Backend
- FastAPI
- SQLAlchemy (SQLite)
- OpenRouter API (DeepSeek R1 Integration)

### Frontend
- Modern HTML/CSS/JavaScript
- Responsive Design (Mobile Tabs)

### DevOps
- AWS EC2
- GitHub Pages

---

## 🌐 Deployment

### Frontend (GitHub Pages)
Automatically deployed via GitHub Actions when pushing to `main` branch.

### Backend (AWS EC2)

**Deployment is currently manual.**
See "Quick Start" above.

---

## ❗ Known Issues

### Chat 500 Internal Server Error
Sometimes the chat interface may return an "Internal Server Error" when communicating with the AI model.
- **Workaround:** Ensure the backend service is running and the OpenRouter API key is valid. If the error persists, check `backend.log` for details.
- **Status:** Pending investigation (Low Priority).

---

## 📊 API Documentation

Once the backend is running, visit:
- **Local:** http://localhost:8000/docs
- **Production:** http://<YOUR_EC2_IP>:8000/docs

---

## 🔒 Security Notes

- ✅ All secrets stored in GitHub Secrets (not in code)
- ✅ `.env` files in `.gitignore`
- ✅ CORS configured for specific origins
- ✅ Session-based document isolation

**Never commit:**
- API keys
- Database credentials
- Private keys
- `.env` files

---

## 📝 License

MIT License - See individual project folders for details.

---

## 👤 Author

**Ibrahim**
- GitHub: [@1brah1](https://github.com/1brah1)
- Portfolio: https://1brah1.github.io/cs_stuff/

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

**Last Updated:** January 2026
