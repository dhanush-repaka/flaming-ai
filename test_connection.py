#!/usr/bin/env python3
"""
Test script to verify connection to LLAMA LLM service
"""

from llama_client import LlamaClient
import json

def test_llama_connection():
    """Test the connection to LLAMA LLM service"""
    print("🔗 Testing LLAMA LLM Connection...")
    print("=" * 50)
    
    try:
        # Initialize the client
        client = LlamaClient()
        
        # Test 1: Authentication
        print("1. Testing Authentication...")
        try:
            token = client.get_access_token()
            print("✅ Authentication successful!")
            print(f"   Token obtained: {token[:50]}...")
        except Exception as e:
            print(f"❌ Authentication failed: {str(e)}")
            return
        
        # Test 2: Connection test
        print("\n2. Testing Service Connection...")
        connection_result = client.test_connection()
        
        if connection_result["status"] == "success":
            print("✅ Connection successful!")
            print(f"   Response: {connection_result.get('response', 'No response data')}")
        else:
            print(f"❌ Connection failed: {connection_result['message']}")
            print("   Note: The service might not have a /health endpoint.")
            print("   This doesn't necessarily mean the service is unavailable.")
        
        # Test 3: Get available models
        print("\n3. Testing Models Endpoint...")
        models_result = client.get_available_models()
        
        if models_result["status"] == "success":
            print("✅ Models endpoint accessible!")
            models = models_result.get("models", {})
            if "data" in models:
                print(f"   Available models: {len(models['data'])}")
                for model in models["data"][:3]:  # Show first 3 models
                    print(f"   - {model.get('id', 'Unknown')}")
            else:
                print(f"   Models response: {models}")
        else:
            print(f"❌ Models endpoint failed: {models_result['message']}")
        
        # Test 4: Simple chat test
        print("\n4. Testing Chat Functionality...")
        chat_result = client.send_chat_message("Hello! Can you respond with a simple greeting?")
        
        if chat_result["status"] == "success":
            print("✅ Chat functionality working!")
            print(f"   Response: {chat_result['message'][:100]}...")
        else:
            print(f"❌ Chat functionality failed: {chat_result['message']}")
        
        print("\n" + "=" * 50)
        print("🎉 Connection test completed!")
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    test_llama_connection() 