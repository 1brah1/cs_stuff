# AI Document Reviewer

An AI-powered document review application built with FastAPI, React, TypeScript, and PostgreSQL. This application uses DeepSeek R1T2 via OpenRouter API to provide comprehensive document reviews and feedback.

## Features

- **Document Upload**: Upload text (.txt) and PDF files for review
- **AI-Powered Reviews**: Get detailed feedback using DeepSeek R1T2 model
- **Review History**: Track and view all past document reviews
- **Authentication**: Simple JWT-based authentication (demo mode)
- **CI/CD**: Automated testing and deployment with GitHub Actions
- **Responsive Design**: Modern, mobile-friendly UI

## Architecture

- **Backend**: FastAPI (Python) with PostgreSQL
- **Frontend**: React with TypeScript
- **AI Service**: OpenRouter API (DeepSeek R1T2)
- **Deployment**: Render (backend) + GitHub Pages (frontend)
- **CI/CD**: GitHub Actions workflows

## Project Structure

```
AI-solver-reviewer/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # API endpoints
│   │   ├── core/                # Configuration
│   │   ├── db/                  # Database setup
│   │   ├── models/              # SQLAlchemy models
│   │   ├── services/            # Business logic (OpenRouter)
│   │   └── main.py              # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API service
│   │   └── App.tsx
│   ├── package.json
│   └── public/
└── .github/workflows/           # CI/CD workflows
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- OpenRouter API key
- Render account (for deployment)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/ai_reviewer_db
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

5. Set up database:
```bash
# Create database
createdb ai_reviewer_db

# Tables are created automatically on first run
```

6. Run the backend:
```bash
python run.py
```

Backend will be available at `http://localhost:8000`
API docs available at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```env
REACT_APP_API_URL=http://localhost:8000
```

4. Start development server:
```bash
npm start
```

Frontend will be available at `http://localhost:3000`

## Deployment

### Backend Deployment (Render)

1. Create a new PostgreSQL database on Render
2. Create a new Web Service for the backend
3. Connect your GitHub repository
4. Configure environment variables on Render:
   - `DATABASE_URL` (from Render PostgreSQL)
   - `OPENROUTER_API_KEY`
   - `JWT_SECRET_KEY`
   - `FRONTEND_URL` (your GitHub Pages URL)
   - `ENVIRONMENT=production`
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment (GitHub Pages)

1. Enable GitHub Pages in repository settings
2. Configure the workflow to deploy from `main` branch
3. Set `REACT_APP_API_URL` secret in GitHub repository settings (your Render backend URL)
4. The workflow will automatically deploy on push to `main`

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login (demo)
- `GET /api/v1/auth/me` - Get current user

### Documents
- `POST /api/v1/documents/upload` - Upload a document
- `GET /api/v1/documents` - List all documents
- `GET /api/v1/documents/{id}` - Get document details

### Reviews
- `POST /api/v1/reviews/{document_id}` - Create AI review
- `GET /api/v1/reviews/{document_id}` - Get reviews for a document
- `GET /api/v1/reviews` - Get all reviews

## GitHub Actions Workflows

- **ci-backend.yml**: Backend testing and linting
- **ci-frontend.yml**: Frontend type checking and build
- **deploy-backend.yml**: Backend deployment trigger
- **deploy-frontend.yml**: Frontend deployment to GitHub Pages
- **security-scan.yml**: Security vulnerability scanning

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `OPENROUTER_API_KEY`: OpenRouter API key
- `JWT_SECRET_KEY`: Secret key for JWT tokens
- `FRONTEND_URL`: Frontend URL for CORS
- `ENVIRONMENT`: `development` or `production`

### Frontend
- `REACT_APP_API_URL`: Backend API URL

## Development

### Running Tests

Backend:
```bash
cd backend
pytest
```

Frontend:
```bash
cd frontend
npm test
```

### Database Migrations

Tables are created automatically using SQLAlchemy. For production migrations, consider using Alembic (already included in requirements).

## Security Notes

- Currently uses simplified authentication for demo purposes
- In production, implement proper JWT token validation
- Store API keys securely using environment variables
- Use HTTPS in production
- Implement rate limiting for API endpoints

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions, please open an issue on GitHub.

