from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db
from app.models.document import Document
from app.services.openrouter_service import OpenRouterService
from app.core.session import get_session_id
from datetime import datetime
from typing import List

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Chat with AI about uploaded documents
    """
    # Get documents for this session
    documents = db.query(Document).filter(
        Document.session_id == request.session_id,
        Document.expires_at > datetime.utcnow()
    ).all()
    
    if not documents:
        return ChatResponse(
            response="Please upload at least one document before starting a chat. I can help you analyze PDF and TXT files."
        )
    
    # Build context from documents
    context = "Here are the documents you uploaded:\n\n"
    for doc in documents:
        context += f"--- {doc.filename} ---\n{doc.content[:2000]}\n\n"
    
    context += f"\nUser question: {request.message}"
    
    try:
        # Call OpenRouter API
        openrouter = OpenRouterService()
        ai_response = await openrouter.generate_response(context)
        
        return ChatResponse(response=ai_response)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {str(e)}"
        )


@router.post("/session/{session_id}/cleanup")
async def cleanup_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Clean up session data when user closes browser
    """
    try:
        # Delete documents for this session
        db.query(Document).filter(
            Document.session_id == session_id
        ).delete()
        
        db.commit()
        
        return {"message": "Session cleaned up successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Cleanup error: {str(e)}"
        )
