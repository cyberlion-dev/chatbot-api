#!/usr/bin/env python3
"""
Simple test script to verify the chatbot API is working
Run this after starting the server locally
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_health_check():
    """Test the health endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False
    return True

def test_chat_endpoint():
    """Test the chat endpoint"""
    print("\n🤖 Testing chat endpoint...")
    
    test_messages = [
        "Hello, how are you today?",
        "What are your business hours?",
        "Can you help me with pricing?",
        "Tell me about your services",
    ]
    
    conversation_id = None
    conversation_history = []
    
    for message in test_messages:
        print(f"\n💬 Sending: {message}")
        
        payload = {
            "message": message,
            "conversation_id": conversation_id,
            "conversation_history": conversation_history
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{API_BASE}/api/v1/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"🤖 Response: {data['response']}")
                print(f"⏱️  Processing time: {data['processing_time']:.2f}s")
                print(f"🔗 Conversation ID: {data['conversation_id']}")
                
                # Update conversation tracking
                conversation_id = data['conversation_id']
                conversation_history.extend([
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": data['response']}
                ])
                
            else:
                print(f"❌ Chat failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
            return False
    
    return True

def test_config_endpoint():
    """Test the config endpoint"""
    print("\n⚙️  Testing config endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/v1/config")
        if response.status_code == 200:
            config = response.json()
            print("✅ Config retrieved successfully")
            print(f"   Business: {config['business_config']['name']}")
            print(f"   Type: {config['business_config']['type']}")
            print(f"   Model: {config['model_info']['name']}")
        else:
            print(f"❌ Config failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False
    return True

def main():
    """Run all tests"""
    print("🧪 AI Chatbot API Test Suite")
    print("=" * 40)
    
    # Test health first
    if not test_health_check():
        print("\n❌ Health check failed, aborting tests")
        print("Make sure the server is running: uvicorn app.main:app --reload")
        return
    
    # Test other endpoints
    chat_success = test_chat_endpoint()
    config_success = test_config_endpoint()
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    print(f"   Health Check: ✅")
    print(f"   Chat Endpoint: {'✅' if chat_success else '❌'}")
    print(f"   Config Endpoint: {'✅' if config_success else '❌'}")
    
    if chat_success and config_success:
        print("\n🎉 All tests passed! Your API is ready for deployment.")
    else:
        print("\n⚠️  Some tests failed. Check the logs above.")

if __name__ == "__main__":
    main()