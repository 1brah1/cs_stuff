#!/usr/bin/env python3
"""
Test script to verify backend setup
"""
import os
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import fastapi
        print("✓ FastAPI")
        import sqlalchemy
        print("✓ SQLAlchemy")
        import uvicorn
        print("✓ Uvicorn")
        from app.core.config import settings
        print(f"✓ Config loaded - Database: {settings.DATABASE_URL}")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_database():
    """Test database connection"""
    print("\nTesting database...")
    try:
        from app.db.database import engine, Base
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created")
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_api():
    """Test if API can start"""
    print("\nTesting API...")
    try:
        from app.main import app
        print("✓ API app created")
        return True
    except Exception as e:
        print(f"✗ API test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Backend Setup Test")
    print("=" * 50)
    
    # Create data directory
    data_dir = backend_dir / "data"
    data_dir.mkdir(exist_ok=True)
    print(f"✓ Data directory: {data_dir}")
    
    # Run tests
    tests = [
        test_imports(),
        test_database(),
        test_api()
    ]
    
    print("\n" + "=" * 50)
    if all(tests):
        print("✅ All tests passed! Backend is ready.")
        print("\nTo start the server, run:")
        print("  python run.py")
    else:
        print("❌ Some tests failed. Check errors above.")
        sys.exit(1)
