from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.document import Document
from app.models.review import Review
from app.services.openrouter_service import OpenRouterService
from app.core.session import get_session_id, get_session_expiration
from pydantic import BaseModel
from datetime import datetime
import PyPDF2
import io

router = APIRouter()


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    created_at: datetime
    review_count: int = 0
    
    class Config:
        from_attributes = True


class DocumentDetailResponse(DocumentResponse):
    content: str
    reviews: List[dict] = []


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    session_id: str = Depends(get_session_id),
):
    """
    Upload a document (text or PDF) for review
    """
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    file_type = file.filename.split(".")[-1].lower()
    if file_type not in ["txt", "pdf"]:
        raise HTTPException(
            status_code=400,
            detail="Only .txt and .pdf files are supported"
        )
    
    # Read file content
    contents = await file.read()
    
    # Extract text content
    if file_type == "pdf":
        try:
            pdf_file = io.BytesIO(contents)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"
            content = text_content.strip()
            if not content:
                raise HTTPException(
                    status_code=400,
                    detail="Could not extract text from PDF. The PDF might be image-based."
                )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error reading PDF: {str(e)}"
            )
    else:
        content = contents.decode("utf-8")
    
    # Create document record with session tracking and expiration
    db_document = Document(
        filename=file.filename,
        file_type=file_type,
        content=content,
        session_id=session_id,
        expires_at=get_session_expiration(hours=1)
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return DocumentResponse(
        id=db_document.id,
        filename=db_document.filename,
        file_type=db_document.file_type,
        created_at=db_document.created_at,
        review_count=0
    )


@router.get("/", response_model=List[DocumentResponse])
async def get_documents(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    session_id: str = Depends(get_session_id)
):
    """
    Get list of uploaded documents for current session with pagination
    """
    # Filter by session ID and exclude expired documents
    documents = db.query(Document).filter(
        Document.session_id == session_id,
        Document.expires_at > datetime.utcnow()
    ).offset(skip).limit(limit).all()
    
    result = []
    for doc in documents:
        review_count = db.query(Review).filter(Review.document_id == doc.id).count()
        result.append(DocumentResponse(
            id=doc.id,
            filename=doc.filename,
            file_type=doc.file_type,
            created_at=doc.created_at,
            review_count=review_count
        ))
    
    return result


@router.get("/{document_id}", response_model=DocumentDetailResponse)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific document by ID
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    reviews = db.query(Review).filter(Review.document_id == document_id).all()
    
    return DocumentDetailResponse(
        id=document.id,
        filename=document.filename,
        file_type=document.file_type,
        content=document.content,
        created_at=document.created_at,
        review_count=len(reviews),
        reviews=[{
            "id": r.id,
            "review_text": r.review_text,
            "status": r.status,
            "created_at": r.created_at.isoformat()
        } for r in reviews]
    )









