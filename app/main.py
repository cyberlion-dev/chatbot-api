"""
AI Chatbot API - FastAPI + LangChain + HuggingFace
A proof of concept for business-context chatbots
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import os
from app.api.chat import router as chat_router
from app.core.config import settings
from app.services.ai_service import AIService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global AI service instance
ai_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global ai_service
    
    # Startup
    logger.info("🚀 Starting AI Chatbot API...")
    try:
        ai_service = AIService()
        await ai_service.initialize()
        logger.info("✅ AI Service initialized successfully")
        app.state.ai_service = ai_service
    except Exception as e:
        logger.error(f"❌ Failed to initialize AI service: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down AI Chatbot API...")

# Create FastAPI app
app = FastAPI(
    title="AI Chatbot API",
    description="Business-context chatbot with LangChain and HuggingFace",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
# Convert comma-separated ALLOWED_ORIGINS to list
allowed_origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Chatbot API is running! 🤖",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        # Check if AI service is available
        if not hasattr(app.state, 'ai_service') or app.state.ai_service is None:
            raise HTTPException(status_code=503, detail="AI service not available")
            
        return {
            "status": "healthy",
            "ai_service": "available",
            "model": app.state.ai_service.model_name if app.state.ai_service else "unknown"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=False
    )