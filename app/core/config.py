"""
Application configuration settings
"""

import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Chatbot API"
    PORT: int = 8000

    # CORS
    ALLOWED_ORIGINS: str = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:3001"
    )
    
    # AI Model Settings
    MODEL_NAME: str = os.getenv("MODEL_NAME", "microsoft/DialoGPT-medium")
    MODEL_DEVICE: int = int(os.getenv("MODEL_DEVICE", -1))  # -1 for CPU, 0 for GPU
    MAX_LENGTH: int = int(os.getenv("MAX_LENGTH", 512))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", 0.7))
    
    # Business Context
    BUSINESS_NAME: str = os.getenv("BUSINESS_NAME", "Demo Business")
    BUSINESS_TYPE: str = os.getenv("BUSINESS_TYPE", "customer service")

    # Detailed business information (hours, location, services, pricing, etc.)
    BUSINESS_DETAILS: str = os.getenv(
        "BUSINESS_DETAILS",
        "No specific business details configured yet."
    )

    # Allowed topics (comma-separated)
    ALLOWED_TOPICS: str = os.getenv(
        "ALLOWED_TOPICS",
        "general questions,product information,pricing,support"
    )

    # Restricted topics (comma-separated)
    RESTRICTED_TOPICS: str = os.getenv(
        "RESTRICTED_TOPICS",
        "medical advice,legal advice,financial advice,personal information"
    )
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", 100))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", 3600))  # seconds
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()