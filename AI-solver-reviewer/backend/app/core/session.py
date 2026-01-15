"""Session management utilities for temporary document storage."""
import uuid
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Header, HTTPException


def generate_session_id() -> str:
    """Generate a unique session ID."""
    return str(uuid.uuid4())


def get_session_expiration(hours: int = 1) -> datetime:
    """Get expiration datetime for session data.
    
    Args:
        hours: Number of hours until expiration (default: 1)
    
    Returns:
        Datetime object for expiration time
    """
    return datetime.utcnow() + timedelta(hours=hours)


async def get_session_id(x_session_id: Optional[str] = Header(None)) -> str:
    """Dependency to get and validate session ID from request headers.
    
    Args:
        x_session_id: Session ID from X-Session-Id header
    
    Returns:
        Validated session ID
    
    Raises:
        HTTPException: If session ID is missing or invalid
    """
    if not x_session_id:
        raise HTTPException(
            status_code=400,
            detail="Session ID required. Include X-Session-Id header."
        )
    
    # Basic validation
    try:
        uuid.UUID(x_session_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid session ID format"
        )
    
    return x_session_id
