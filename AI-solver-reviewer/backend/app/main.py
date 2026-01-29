from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.db.database import engine, Base
from app.services.cleanup import cleanup_expired_data
from apscheduler.schedulers.background import BackgroundScheduler
import logging

logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Document Reviewer API",
    description="API for AI-powered document review using DeepSeek R1T2",
    version="1.0.0"
)

# Configure CORS - Allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Initialize cleanup scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_expired_data, 'interval', minutes=15)


@app.on_event("startup")
async def startup_event():
    """Start the cleanup scheduler on application startup."""
    scheduler.start()
    logger.info("Started background cleanup scheduler (runs every 15 minutes)")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown the cleanup scheduler on application shutdown."""
    scheduler.shutdown()
    logger.info("Stopped background cleanup scheduler")


@app.get("/")
async def root():
    return {"message": "AI Document Reviewer API", "status": "healthy"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

