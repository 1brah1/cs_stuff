# AI Document Reviewer - Simple Frontend

This is a lightweight, standalone frontend for the AI Document Reviewer that can be deployed alongside the FastAPI backend on EC2.

## Features

- Upload PDF and TXT documents
- Chat with AI (DeepSeek) about uploaded documents
- Session-based document management
- Automatic cleanup when browser closes
- Modern dark-themed UI
- No authentication required

## Files

- `index.html` - Main application HTML
- `app-style.css` - Styling
- `app-script.js` - JavaScript functionality

## Deployment to EC2

### Option 1: Serve with Python HTTP Server

```bash
# On EC2 instance
cd AI-solver-reviewer/frontend-simple
python3 -m http.server 8080
```

Then access at: `http://13.211.53.117:8080`

### Option 2: Serve with Nginx

```bash
# Install nginx
sudo apt update
sudo apt install nginx

# Copy files to nginx directory
sudo cp -r /path/to/frontend-simple/* /var/www/html/ai-reviewer/

# Configure nginx to serve on port 8080
sudo nano /etc/nginx/sites-available/ai-reviewer
```

Add this configuration:

```nginx
server {
    listen 8080;
    server_name 13.211.53.117;

    root /var/www/html/ai-reviewer;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to backend
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/ai-reviewer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 3: Serve from FastAPI Backend

Add this to your FastAPI `main.py`:

```python
from fastapi.staticfiles import StaticFiles

# After creating the app
app.mount("/app", StaticFiles(directory="frontend-simple", html=True), name="app")
```

Then access at: `http://13.211.53.117:8000/app/`

## Local Development

1. Start the backend:
```bash
cd AI-solver-reviewer/backend
python run.py
```

2. Serve the frontend:
```bash
cd AI-solver-reviewer/frontend-simple
python -m http.server 3000
```

3. Open `http://localhost:3000` in your browser

The frontend will automatically connect to `localhost:8000` when running locally, or to `13.211.53.117:8000` when deployed.

## How It Works

1. **Session Management**: When you open the app, a unique session ID is generated
2. **Document Upload**: Upload PDF or TXT files which are processed and stored with your session ID
3. **AI Chat**: Ask questions and the AI will respond based on your uploaded documents
4. **Auto Cleanup**: When you close the browser, your session data is automatically deleted

## API Endpoints Used

- `POST /api/v1/documents/upload` - Upload documents
- `POST /api/v1/chat` - Chat with AI
- `POST /api/v1/session/{session_id}/cleanup` - Clean up session

## Requirements

The backend must be running and accessible at:
- Local: `http://localhost:8000`
- Production: `http://13.211.53.117:8000`

Make sure your backend has:
- CORS enabled for the frontend origin
- OpenRouter API key configured
- The chat endpoint available
