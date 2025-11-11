"""
Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    """Single chat message"""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = Field(default=None, description="Message timestamp")

class ChatRequest(BaseModel):
    """Chat request payload"""
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    conversation_id: Optional[str] = Field(default=None, description="Conversation ID for context")
    context: Optional[str] = Field(default=None, description="Additional context")
    conversation_history: Optional[List[ChatMessage]] = Field(default=[], description="Previous messages")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What are your business hours?",
                "conversation_id": "abc123",
                "conversation_history": [
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi! How can I help you today?"}
                ]
            }
        }

class ChatResponse(BaseModel):
    """Chat response payload"""
    response: str = Field(..., description="AI assistant response")
    conversation_id: str = Field(..., description="Conversation ID")
    model_used: str = Field(..., description="AI model that generated the response")
    processing_time: float = Field(..., description="Response processing time in seconds")
    tokens_used: Optional[int] = Field(default=None, description="Number of tokens used")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Our business hours are 9 AM to 6 PM, Monday through Friday.",
                "conversation_id": "abc123",
                "model_used": "microsoft/DialoGPT-medium",
                "processing_time": 1.23,
                "tokens_used": 45
            }
        }

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(default=None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")

class BusinessConfig(BaseModel):
    """Business configuration model"""
    name: str = Field(..., description="Business name")
    type: str = Field(..., description="Business type")
    allowed_topics: List[str] = Field(..., description="Topics the bot can discuss")
    restricted_topics: List[str] = Field(..., description="Topics the bot should avoid")
    
class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    ai_service: str = Field(..., description="AI service status")
    model: str = Field(..., description="Current model name")
    uptime: Optional[str] = Field(default=None, description="Service uptime")