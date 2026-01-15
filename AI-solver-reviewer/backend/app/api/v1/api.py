from fastapi import APIRouter
from app.api.v1.endpoints import documents, reviews, auth

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])





