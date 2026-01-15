"""Background service for cleaning up expired documents and reviews."""
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.document import Document
from app.models.review import Review

logger = logging.getLogger(__name__)


def cleanup_expired_data():
    """Delete expired documents and reviews from database.
    
    This runs as a background task to clean up temporary session data.
    """
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        
        # Delete expired reviews (cascade will delete associated reviews)
        deleted_reviews = db.query(Review).filter(
            Review.expires_at <= now
        ).delete(synchronize_session=False)
        
        # Delete expired documents
        deleted_docs = db.query(Document).filter(
            Document.expires_at <= now
        ).delete(synchronize_session=False)
        
        db.commit()
        
        if deleted_docs > 0 or deleted_reviews > 0:
            logger.info(
                f"Cleanup completed: deleted {deleted_docs} documents "
                f"and {deleted_reviews} reviews"
            )
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
        db.rollback()
    finally:
        db.close()
