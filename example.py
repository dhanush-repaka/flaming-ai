#!/usr/bin/env python3
"""
Simple example of using the LLAMA LLM client
"""

from llama_client import LlamaClient
import json

def main():
    print("🚀 LLAMA LLM Client Example")
    print("=" * 40)
    
    # Initialize the client
    client = LlamaClient()
    
    try:
        # Step 1: Test authentication
        print("1. Testing authentication...")
        token = client.get_access_token()
        print(f"✅ Authentication successful! Token: {token[:30]}...")
        
        # Step 2: Test connection
        print("\n2. Testing connection...")
        connection_result = client.test_connection()
        if connection_result["status"] == "success":
            print("✅ Connection successful!")
        else:
            print(f"⚠️ Connection test: {connection_result['message']}")
        
        # Step 3: Get available models
        print("\n3. Getting available models...")
        models_result = client.get_available_models()
        if models_result["status"] == "success":
            print("✅ Models retrieved successfully!")
            models = models_result.get("models", {})
            if "data" in models and models["data"]:
                print("Available models:")
                for model in models["data"][:3]:  # Show first 3
                    print(f"  - {model.get('id', 'Unknown')}")
            else:
                print("No models found or different response format")
        else:
            print(f"⚠️ Models endpoint: {models_result['message']}")
        
        # Step 4: Simple chat
        print("\n4. Testing chat functionality...")
        chat_result = client.send_chat_message("Hello! Please respond with a brief greeting.")
        
        if chat_result["status"] == "success":
            print("✅ Chat successful!")
            print(f"Response: {chat_result['message']}")
        else:
            print(f"❌ Chat failed: {chat_result['message']}")
        
        # Step 5: Conversation example
        print("\n5. Testing conversation...")
        conversation = [
            {"role": "user", "content": "What is the capital of France?"},
            {"role": "assistant", "content": "The capital of France is Paris."},
            {"role": "user", "content": "What is the population of Paris?"}
        ]
        
        response = client.send_chat_message("What is the population of Paris?", conversation)
        
        if response["status"] == "success":
            print("✅ Conversation successful!")
            print(f"Response: {response['message']}")
        else:
            print(f"❌ Conversation failed: {response['message']}")
        
        print("\n" + "=" * 40)
        print("🎉 Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 