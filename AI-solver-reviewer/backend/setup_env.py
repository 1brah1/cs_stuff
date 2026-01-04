#!/usr/bin/env python3
"""
Setup script to create .env file with API keys
Run this script to initialize your environment variables
"""

import os
from pathlib import Path

def create_env_file():
    backend_dir = Path(__file__).parent
    env_file = backend_dir / ".env"
    
    # API keys (you can modify these)
    openrouter_key = "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"
    
    env_content = f"""# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_reviewer_db

# OpenRouter API
OPENROUTER_API_KEY={openrouter_key}

# JWT Secret (generate a new one for production)
JWT_SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
JWT_ALGORITHM=HS256

# CORS
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
"""
    
    if env_file.exists():
        print(f".env file already exists at {env_file}")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Skipping .env file creation")
            return
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"Created .env file at {env_file}")
    print("\n⚠️  IMPORTANT: Update DATABASE_URL with your actual PostgreSQL connection string")
    print("⚠️  For production, change JWT_SECRET_KEY to a secure random value")

if __name__ == "__main__":
    create_env_file()


