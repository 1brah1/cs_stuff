from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import get_db
from pydantic import BaseModel

router = APIRouter()
security = HTTPBearer()


# Simplified auth for demo - in production, use proper JWT
class UserSession(BaseModel):
    user_id: int = 1
    username: str = "demo_user"


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UserSession:
    """
    Simplified authentication - accepts any bearer token for demo
    In production, validate JWT token here
    """
    # For demo purposes, accept any token
    # In production: validate JWT token and return actual user
    return UserSession(user_id=1, username="demo_user")


@router.post("/login")
async def login(username: str = "demo_user", password: str = "demo"):
    """
    Simplified login endpoint for demo
    In production, implement proper authentication
    """
    # For demo, return a mock token
    return {
        "access_token": "demo_token_12345",
        "token_type": "bearer",
        "user": {"id": 1, "username": "demo_user"}
    }


@router.get("/me")
async def get_current_user_info(current_user: UserSession = Depends(get_current_user)):
    return current_user





