from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.document import Document
from app.models.review import Review
from app.services.openrouter_service import OpenRouterService
from app.api.v1.endpoints.auth import get_current_user
from app.core.session import get_session_id, get_session_expiration
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()
openrouter_service = OpenRouterService()


class ReviewResponse(BaseModel):
    id: int
    document_id: int
    review_text: str
    status: str
    created_at: datetime
    document_filename: str = ""
    
    class Config:
        from_attributes = True


class CreateReviewResponse(BaseModel):
    id: int
    document_id: int
    review_text: str
    status: str
    created_at: datetime


@router.post("/{document_id}", response_model=CreateReviewResponse)
async def create_review(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    session_id: str = Depends(get_session_id)
):
    """
    Create an AI review for a document
    """
    # Get document and verify it belongs to this session
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.session_id == session_id,
        Document.expires_at > datetime.utcnow()
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Call OpenRouter API for review
    try:
        review_text = await openrouter_service.review_document(document.content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating review: {str(e)}"
        )
    
    # Create review record with expiration matching document
    db_review = Review(
        document_id=document_id,
        review_text=review_text,
        status="completed",
        expires_at=document.expires_at
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    return CreateReviewResponse(
        id=db_review.id,
        document_id=db_review.document_id,
        review_text=db_review.review_text,
        status=db_review.status,
        created_at=db_review.created_at
    )


@router.get("/{document_id}", response_model=List[ReviewResponse])
async def get_reviews(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all reviews for a document
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    reviews = db.query(Review).filter(Review.document_id == document_id).all()
    
    return [
        ReviewResponse(
            id=r.id,
            document_id=r.document_id,
            review_text=r.review_text,
            status=r.status,
            created_at=r.created_at,
            document_filename=document.filename
        )
        for r in reviews
    ]


@router.get("/", response_model=List[ReviewResponse])
async def get_all_reviews(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    session_id: str = Depends(get_session_id)
):
    """
    Get all reviews for current session's documents with pagination
    """
    # Get all reviews for documents in this session that haven't expired
    reviews = db.query(Review).join(Document).filter(
        Document.session_id == session_id,
        Review.expires_at > datetime.utcnow()
    ).offset(skip).limit(limit).all()
    
    result = []
    for review in reviews:
        document = db.query(Document).filter(Document.id == review.document_id).first()
        result.append(ReviewResponse(
            id=review.id,
            document_id=review.document_id,
            review_text=review.review_text,
            status=review.status,
            created_at=review.created_at,
            document_filename=document.filename if document else ""
        ))
    
    return result






