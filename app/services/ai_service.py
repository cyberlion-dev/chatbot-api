"""
AI Service - Core chatbot logic with HuggingFace and LangChain
"""

import asyncio
import logging
import time
import uuid
from typing import List, Dict, Optional, Tuple
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
from app.core.config import settings
from app.models.chat import ChatMessage

logger = logging.getLogger(__name__)

class AIService:
    """Core AI service handling chat interactions"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.model_name = settings.MODEL_NAME
        self.device = settings.MODEL_DEVICE
        self.conversation_memory: Dict[str, List[ChatMessage]] = {}
        self.business_config = self._load_business_config()
        
    async def initialize(self):
        """Initialize the AI model"""
        logger.info(f"🤖 Loading model: {self.model_name}")
        
        try:
            # Determine device
            device_name = "cpu" if self.device == -1 else f"cuda:{self.device}"
            logger.info(f"📱 Using device: {device_name}")
            
            # For lightweight deployment, use pipeline
            # This is more memory efficient than loading model + tokenizer separately
            self.pipeline = pipeline(
                "text-generation",
                model=self.model_name,
                device=self.device,
                torch_dtype=torch.float16 if self.device >= 0 else torch.float32,
                pad_token_id=50256,  # GPT-2 pad token
                do_sample=True,
                temperature=settings.TEMPERATURE,
                max_length=settings.MAX_LENGTH,
                return_full_text=False
            )
            
            logger.info("✅ Model loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            # Fallback to a smaller model
            logger.info("🔄 Falling back to smaller model...")
            try:
                self.model_name = "microsoft/DialoGPT-small"
                self.pipeline = pipeline(
                    "text-generation",
                    model=self.model_name,
                    device=-1,  # Force CPU for fallback
                    pad_token_id=50256,
                    do_sample=True,
                    temperature=0.7,
                    max_length=256,
                    return_full_text=False
                )
                logger.info("✅ Fallback model loaded successfully")
            except Exception as fallback_error:
                logger.error(f"❌ Fallback model failed: {fallback_error}")
                raise
    
    def _load_business_config(self) -> Dict:
        """Load business configuration from settings"""
        return {
            "name": settings.BUSINESS_NAME,
            "type": settings.BUSINESS_TYPE,
            "allowed_topics": [topic.strip() for topic in settings.ALLOWED_TOPICS.split(",")],
            "restricted_topics": [topic.strip() for topic in settings.RESTRICTED_TOPICS.split(",")]
        }
    
    def _is_on_topic(self, message: str) -> Tuple[bool, Optional[str]]:
        """Check if message is within allowed topics"""
        message_lower = message.lower()

        # Check for restricted topics
        for restricted in self.business_config["restricted_topics"]:
            if restricted.lower() in message_lower:
                return False, f"I can't provide {restricted}. Let me help you with {self.business_config['type']} related questions instead."

        # For now, allow all non-restricted topics
        # You can add more sophisticated topic classification here
        return True, None

    def _get_direct_answer(self, message: str) -> Optional[str]:
        """Check if we can provide a direct answer from business details"""
        message_lower = message.lower()
        business_details = settings.BUSINESS_DETAILS.lower()

        # Define keyword patterns for common questions
        patterns = {
            "hours": ["hours", "open", "close", "when are you open", "what time"],
            "location": ["location", "address", "where are you", "where located"],
            "contact": ["contact", "phone", "email", "call", "reach"],
            "pricing": ["price", "cost", "how much", "pricing", "plan"],
            "shipping": ["shipping", "delivery", "ship"],
            "returns": ["return", "refund", "money back"],
            "services": ["service", "what do you do", "what do you offer"],
        }

        # Check if message matches any pattern
        for topic, keywords in patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                # Extract relevant information from BUSINESS_DETAILS
                details_full = settings.BUSINESS_DETAILS

                # For hours
                if topic == "hours" and "hours:" in business_details:
                    start = details_full.lower().find("hours:")
                    end = details_full.find(".", start) if "." in details_full[start:] else len(details_full)
                    return f"Our {details_full[start:end].strip()}. Is there anything else you'd like to know?"

                # For location
                if topic == "location" and "location:" in business_details:
                    start = details_full.lower().find("location:")
                    end = details_full.find(".", start) if "." in details_full[start:] else len(details_full)
                    return f"We're located at: {details_full[start+9:end].strip()}. Feel free to visit us!"

                # For contact
                if topic == "contact" and ("phone" in business_details or "email" in business_details):
                    contact_info = []
                    if "phone" in business_details:
                        start = details_full.lower().find("phone")
                        end = details_full.find(",", start) if "," in details_full[start:start+50] else start+40
                        contact_info.append(details_full[start:end].strip())
                    if "email" in business_details:
                        start = details_full.lower().find("email")
                        end = details_full.find(".", start) if "." in details_full[start:start+50] else start+40
                        contact_info.append(details_full[start:end].strip())
                    return f"You can reach us at: {', '.join(contact_info)}. We're here to help!"

                # For pricing
                if topic == "pricing" and "pricing:" in business_details:
                    start = details_full.lower().find("pricing:")
                    end = details_full.find(".", start) if "." in details_full[start:] else len(details_full)
                    return f"Our {details_full[start:end].strip()}. Would you like more details on any specific plan?"

                # For shipping
                if topic == "shipping" and "shipping:" in business_details:
                    start = details_full.lower().find("shipping:")
                    end = details_full.find(".", start) if "." in details_full[start:] else len(details_full)
                    return f"Regarding {details_full[start:end].strip()}. Can I help you with anything else?"

                # For returns
                if topic == "returns" and "return" in business_details:
                    start = details_full.lower().find("return")
                    end = details_full.find(".", start) if "." in details_full[start:] else len(details_full)
                    return f"Our return policy: {details_full[start:end].strip()}. Let me know if you have questions!"

                # For services
                if topic == "services" and "services:" in business_details:
                    start = details_full.lower().find("services:")
                    end = details_full.find(".", start) if "." in details_full[start:] else len(details_full)
                    return f"We {details_full[start+9:end].strip()}. What can I help you with today?"

        return None
    
    def _build_conversation_context(self, conversation_history: List[ChatMessage], max_context: int = 3) -> str:
        """Build conversation context from history"""
        if not conversation_history:
            return ""
        
        # Take last few messages for context
        recent_messages = conversation_history[-max_context:]
        context_parts = []
        
        for msg in recent_messages:
            role = "Human" if msg.role == "user" else "Assistant"
            context_parts.append(f"{role}: {msg.content}")
        
        return "\n".join(context_parts)
    
    def _create_business_prompt(self, user_message: str, context: str = "") -> str:
        """Create a business-specific prompt"""
        business_context = f"""You are a helpful assistant for {self.business_config['name']}, a {self.business_config['type']}.

BUSINESS INFORMATION:
{settings.BUSINESS_DETAILS}

GUIDELINES:
- Be professional, helpful, and friendly
- Use the business information above to answer questions accurately
- Focus on topics related to: {', '.join(self.business_config['allowed_topics'])}
- If asked about unrelated topics, politely redirect to your area of expertise
- Keep responses concise and helpful
- End with a helpful question when appropriate

CONVERSATION CONTEXT:
{context}

USER: {user_message}
ASSISTANT:"""

        return business_context
    
    async def chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        conversation_history: Optional[List[ChatMessage]] = None,
        context: Optional[str] = None
    ) -> Dict:
        """Process chat message and return response"""
        start_time = time.time()
        
        # Generate conversation ID if not provided
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        
        # Check topic appropriateness
        is_appropriate, redirect_message = self._is_on_topic(message)
        if not is_appropriate:
            return {
                "response": redirect_message,
                "conversation_id": conversation_id,
                "model_used": "business_rules",
                "processing_time": time.time() - start_time,
                "tokens_used": 0
            }

        # Check if we can provide a direct answer from business details
        direct_answer = self._get_direct_answer(message)
        if direct_answer:
            return {
                "response": direct_answer,
                "conversation_id": conversation_id,
                "model_used": "business_knowledge",
                "processing_time": time.time() - start_time,
                "tokens_used": len(direct_answer.split())
            }

        try:
            # Build conversation context
            if conversation_history:
                conversation_context = self._build_conversation_context(conversation_history)
            else:
                conversation_context = ""
            
            # Add any additional context
            if context:
                conversation_context += f"\nAdditional Context: {context}"
            
            # Create business-specific prompt
            prompt = self._create_business_prompt(message, conversation_context)
            
            # Generate response using the model
            logger.info(f"🤔 Generating response for: {message[:50]}...")
            
            # Run inference
            response = await self._generate_response(prompt)
            
            # Clean up response
            cleaned_response = self._clean_response(response, message)
            
            processing_time = time.time() - start_time
            
            # Store conversation in memory (simple in-memory storage)
            if conversation_id not in self.conversation_memory:
                self.conversation_memory[conversation_id] = []
            
            self.conversation_memory[conversation_id].extend([
                ChatMessage(role="user", content=message),
                ChatMessage(role="assistant", content=cleaned_response)
            ])
            
            # Keep only last 10 messages per conversation
            if len(self.conversation_memory[conversation_id]) > 10:
                self.conversation_memory[conversation_id] = self.conversation_memory[conversation_id][-10:]
            
            return {
                "response": cleaned_response,
                "conversation_id": conversation_id,
                "model_used": self.model_name,
                "processing_time": processing_time,
                "tokens_used": len(cleaned_response.split())  # Rough token estimate
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            return {
                "response": "I apologize, but I'm experiencing technical difficulties. Please try again in a moment.",
                "conversation_id": conversation_id,
                "model_used": "error_handler",
                "processing_time": time.time() - start_time,
                "tokens_used": 0
            }
    
    async def _generate_response(self, prompt: str) -> str:
        """Generate response using the AI model"""
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.pipeline(
                    prompt,
                    max_new_tokens=150,
                    temperature=settings.TEMPERATURE,
                    pad_token_id=self.pipeline.tokenizer.eos_token_id
                )
            )
            
            if response and len(response) > 0:
                return response[0]['generated_text']
            else:
                return "I'm not sure how to respond to that. Could you please rephrase your question?"
                
        except Exception as e:
            logger.error(f"Model generation error: {e}")
            return "I apologize, but I'm having trouble processing your request right now."
    
    def _clean_response(self, response: str, original_message: str) -> str:
        """Clean and post-process the AI response"""
        if not response:
            return "I'm not sure how to respond to that. Could you please rephrase your question?"
        
        # Remove any repetition of the user's message
        cleaned = response.replace(original_message, "").strip()
        
        # Remove common unwanted prefixes
        prefixes_to_remove = ["ASSISTANT:", "Assistant:", "AI:", "Bot:"]
        for prefix in prefixes_to_remove:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()
        
        # Ensure response isn't empty
        if not cleaned:
            cleaned = "I understand your question. How can I help you further?"
        
        # Limit response length
        if len(cleaned) > 500:
            cleaned = cleaned[:500] + "..."
        
        return cleaned
    
    def get_conversation_history(self, conversation_id: str) -> List[ChatMessage]:
        """Retrieve conversation history"""
        return self.conversation_memory.get(conversation_id, [])
    
    def clear_conversation(self, conversation_id: str):
        """Clear specific conversation history"""
        if conversation_id in self.conversation_memory:
            del self.conversation_memory[conversation_id]