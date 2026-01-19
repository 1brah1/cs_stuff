Edit: Right now most of my stuff is not working properly so I will troubleshoot and see what is not working, also will remove unneeded parts of AI document reviewer and shift AWS to https for smoother integeration
# CS Projects Portfolio

A collection of computer science projects showcasing full-stack development, embedded systems, and data analysis.

🌐 **Live Portfolio:** https://1brah1.github.io/cs_stuff/

---

## 📁 Projects

### 🤖 AI Document Reviewer
**Full-stack AI-powered document review application**

- **Backend:** FastAPI + SQLite + OpenRouter API (DeepSeek R1)
- **Frontend:** React + TypeScript
- **Deployment:** AWS EC2 with Docker
- **Features:**
  - Upload PDF/TXT documents
  - AI-powered document analysis
  - Session-based document management
  - RESTful API with automatic documentation

📂 Location: `AI-solver-reviewer/`  
🌐 Live: http://13.211.53.117:8000/docs

---

### 📊 Stock Analysis Portfolio
**Real-time stock market data analysis and visualization**

- **Tech Stack:** Python, yFinance, pandas, matplotlib, SQLite
- **Features:**
  - Real-time stock data collection
  - Automated data pipeline
  - 6 different visualization types
  - Historical data analysis

📂 Location: `stock_analysis_portfolio/`  
🌐 Live: https://1brah1.github.io/cs_stuff/stock-portfolio.html

---

### 🚗 Bluetooth Robot Car
**Arduino-powered robot car with mobile app control**

- **Hardware:** Arduino, HC-05/HC-06 Bluetooth, L298N Motor Driver
- **Software:** React Native mobile app
- **Features:**
  - Wireless Bluetooth control
  - Mobile app interface
  - Real-time motor control

📂 Location: `bluetooth_robot_car/`  
🌐 Live: https://1brah1.github.io/cs_stuff/bluetooth_robot_car/website/

---

## 🚀 Quick Start

### AI Document Reviewer

**Local Development:**
```bash
# Backend
cd AI-solver-reviewer/backend
pip install -r requirements.txt
python setup_env.py  # Enter your OpenRouter API key
python run.py

# Frontend
cd AI-solver-reviewer/frontend
npm install
npm start
```

**Production (EC2):**
```bash
# On EC2 instance
cd ~/ai-reviewer
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🔐 GitHub Secrets Required

For automated deployment via GitHub Actions, set these secrets in your repository:

### Required Secrets:
1. **`OPENROUTER_API_KEY`** - Your OpenRouter API key (get from https://openrouter.ai/)
2. **`JWT_SECRET_KEY`** - Random secret for JWT tokens (generate with `openssl rand -hex 32`)
3. **`EC2_HOST`** - Your EC2 public IP address
4. **`EC2_USERNAME`** - EC2 username (usually `ubuntu`)
5. **`EC2_SSH_KEY`** - Contents of your EC2 private key (.pem file)

### How to Add Secrets:
1. Go to: https://github.com/1brah1/cs_stuff/settings/secrets/actions
2. Click "New repository secret"
3. Add each secret with the exact name above

---

## 📦 Repository Structure

```
cs_stuff/
├── .github/
│   └── workflows/          # GitHub Actions CI/CD
│       ├── deploy-frontend.yml
│       └── deploy-backend.yml
├── AI-solver-reviewer/     # AI Document Reviewer project
│   ├── backend/           # FastAPI backend
│   ├── frontend/          # React frontend
│   └── docker-compose.prod.yml
├── stock_analysis_portfolio/  # Stock analysis project
├── bluetooth_robot_car/   # Robot car project
├── hashtable_implementation/  # C++ data structures
├── KiCad_electronic_schematics/  # PCB designs
├── index.html            # Portfolio homepage
└── README.md            # This file
```

---

## 🛠️ Technologies Used

### Backend
- FastAPI
- SQLAlchemy (SQLite)
- OpenRouter API
- Docker
- JWT Authentication

### Frontend
- React 18
- TypeScript
- Axios
- React Router

### DevOps
- GitHub Actions
- Docker & Docker Compose
- AWS EC2
- GitHub Pages

### Data Analysis
- Python
- pandas
- matplotlib
- yFinance

### Embedded Systems
- Arduino
- React Native
- Bluetooth (HC-05/HC-06)

---

## 🌐 Deployment

### Frontend (GitHub Pages)
Automatically deployed via GitHub Actions when pushing to `main` branch.

**Manual deployment:**
```bash
cd AI-solver-reviewer/frontend
npm run build
cd ../..
# Copy all files to _site folder
mkdir _site
copy index.html _site\
xcopy /E /I AI-solver-reviewer\frontend\build _site\ai-reviewer
# Deploy
cd _site
git init
git add -A
git commit -m "Deploy"
git branch -M gh-pages
git remote add origin https://github.com/1brah1/cs_stuff.git
git push -f origin gh-pages
```

### Backend (AWS EC2)

**Initial Setup:**
1. Launch Ubuntu 22.04 EC2 instance (t2.small or larger)
2. Configure security group (ports: 22, 80, 443, 8000)
3. SSH into instance and install Docker:
```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

**Deploy:**
```bash
# Copy files to EC2
scp -i your-key.pem -r AI-solver-reviewer ubuntu@YOUR_EC2_IP:~/ai-reviewer/

# SSH and start
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
cd ~/ai-reviewer
# Create .env with your secrets
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📊 API Documentation

Once the backend is running, visit:
- **Local:** http://localhost:8000/docs
- **Production:** http://YOUR_EC2_IP:8000/docs

Interactive Swagger UI with all endpoints documented.

---

## 🔒 Security Notes

- ✅ All secrets stored in GitHub Secrets (not in code)
- ✅ `.env` files in `.gitignore`
- ✅ JWT authentication for API
- ✅ CORS configured for specific origins
- ✅ Session-based document isolation

**Never commit:**
- API keys
- Database credentials
- Private keys
- `.env` files

---

## 🐛 Troubleshooting

### AI Reviewer Upload Fails
**Issue:** "Failed to upload file"  
**Solution:** Run locally (`npm start`) as GitHub Pages (HTTPS) can't call HTTP backend.

### Backend Won't Start
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Restart
docker-compose -f docker-compose.prod.yml restart
```

### Database Issues
```bash
# SQLite database is in backend/data/
# To reset: delete backend/data/ai_reviewer.db and restart
```

### Port 8000 Not Accessible
- Check EC2 security group allows inbound TCP 8000
- Verify backend is running: `docker ps`

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

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review project-specific README files
3. Open an issue on GitHub

---

**Last Updated:** January 2026
