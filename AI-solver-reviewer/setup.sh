#!/bin/bash
# Setup script for AI Document Reviewer
# This script creates the necessary .env files

echo "Setting up AI Document Reviewer..."

# Backend .env file
BACKEND_ENV="backend/.env"
if [ -f "$BACKEND_ENV" ]; then
    echo "Backend .env file already exists. Skipping..."
else
    cat > "$BACKEND_ENV" << 'EOF'
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_reviewer_db

# OpenRouter API
OPENROUTER_API_KEY=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

# JWT Secret (generate a new one for production)
JWT_SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
JWT_ALGORITHM=HS256

# CORS
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
EOF
    echo "Created backend/.env file"
fi

# Frontend .env file
FRONTEND_ENV="frontend/.env"
if [ -f "$FRONTEND_ENV" ]; then
    echo "Frontend .env file already exists. Skipping..."
else
    echo "REACT_APP_API_URL=http://localhost:8000" > "$FRONTEND_ENV"
    echo "Created frontend/.env file"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update DATABASE_URL in backend/.env with your PostgreSQL connection string"
echo "2. Install backend dependencies: cd backend && pip install -r requirements.txt"
echo "3. Install frontend dependencies: cd frontend && npm install"
echo "4. Start backend: cd backend && python run.py"
echo "5. Start frontend: cd frontend && npm start"





