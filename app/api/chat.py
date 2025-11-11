"""
Chat API endpoints
"""

import logging
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
import time
from app.models.chat import ChatRequest, ChatResponse, ErrorResponse
from app.services.ai_service import AIService

logger = logging.getLogger(__name__)

router = APIRouter()

def get_ai_service(request: Request) -> AIService:
    """Dependency to get AI service from app state"""
    if not hasattr(request.app.state, 'ai_service') or request.app.state.ai_service is None:
        raise HTTPException(status_code=503, detail="AI service not available")
    return request.app.state.ai_service

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    chat_request: ChatRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Main chat endpoint - send a message and get an AI response
    """
    try:
        logger.info(f"📨 Received chat request: {chat_request.message[:50]}...")
        
        # Process the chat request
        result = await ai_service.chat(
            message=chat_request.message,
            conversation_id=chat_request.conversation_id,
            conversation_history=chat_request.conversation_history,
            context=chat_request.context
        )
        
        # Return formatted response
        return ChatResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ Chat endpoint error: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/conversation/{conversation_id}")
async def get_conversation_history(
    conversation_id: str,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Retrieve conversation history for a specific conversation ID
    """
    try:
        history = ai_service.get_conversation_history(conversation_id)
        return {
            "conversation_id": conversation_id,
            "messages": history,
            "message_count": len(history)
        }
    except Exception as e:
        logger.error(f"❌ Error retrieving conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/conversation/{conversation_id}")
async def clear_conversation(
    conversation_id: str,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Clear conversation history for a specific conversation ID
    """
    try:
        ai_service.clear_conversation(conversation_id)
        return {"message": f"Conversation {conversation_id} cleared successfully"}
    except Exception as e:
        logger.error(f"❌ Error clearing conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/config")
async def get_business_config(ai_service: AIService = Depends(get_ai_service)):
    """
    Get current business configuration
    """
    try:
        return {
            "business_config": ai_service.business_config,
            "model_info": {
                "name": ai_service.model_name,
                "device": "CPU" if ai_service.device == -1 else f"GPU:{ai_service.device}"
            }
        }
    except Exception as e:
        logger.error(f"❌ Error getting config: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test")
async def test_chat():
    """
    Simple test endpoint to verify API is working
    """
    return {
        "message": "Chat API is working! 🎉",
        "timestamp": time.time(),
        "endpoints": {
            "chat": "POST /api/v1/chat",
            "history": "GET /api/v1/conversation/{id}",
            "clear": "DELETE /api/v1/conversation/{id}",
            "config": "GET /api/v1/config"
        }
    }