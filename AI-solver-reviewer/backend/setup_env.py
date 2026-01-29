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
    
    print("Please enter your API keys:")
    openrouter_key = input("OpenRouter API Key: ").strip()
    
    env_content = f"""# Database
DATABASE_URL=sqlite:///./data/ai_reviewer.db

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
    print("\n⚠️  For production, change JWT_SECRET_KEY to a secure random value")

if __name__ == "__main__":
    create_env_file()

