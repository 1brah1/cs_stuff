from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    review_text = Column(Text, nullable=False)
    status = Column(String, default="completed")
    expires_at = Column(DateTime, nullable=False)  # Automatic expiration
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="reviews")





