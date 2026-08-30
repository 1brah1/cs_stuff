from fastapi import APIRouter, HTTPException

router = APIRouter()

DEMO_TOKEN = "demo_token_12345"


@router.post("/login")
async def login(username: str = "demo_user", password: str = "demo"):
    """Demo auth for portfolio use."""
    if username == "demo_user" and password == "demo":
        return {"access_token": DEMO_TOKEN, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
