#!/usr/bin/env python3
"""
Debug script to find the correct API endpoints for the LLAMA service
"""

import requests
import json
from llama_client import LlamaClient

def debug_service_endpoints():
    """Debug the service endpoints to find the correct ones"""
    print("🔍 Debugging LLAMA Service Endpoints")
    print("=" * 50)
    
    try:
        # Initialize client
        client = LlamaClient()
        client.ensure_valid_token()
        
        headers = {
            "Authorization": f"Bearer {client.access_token}",
            "Ocp-Apim-Subscription-Key": client.subscription_key,
            "Content-Type": "application/json"
        }
        
        # Test different endpoints
        endpoints_to_test = [
            "/",
            "/health",
            "/status",
            "/ping",
            "/api/health",
            "/v1/health",
            "/models",
            "/v1/models",
            "/api/models",
            "/chat/completions",
            "/v1/chat/completions",
            "/api/chat/completions",
            "/completions",
            "/v1/completions"
        ]
        
        print("Testing different endpoints...")
        print()
        
        for endpoint in endpoints_to_test:
            try:
                url = f"{client.base_url}{endpoint}"
                print(f"🔧 Testing: {endpoint}")
                
                response = requests.get(url, headers=headers, timeout=10)
                
                print(f"   Status: {response.status_code}")
                print(f"   Content-Type: {response.headers.get('content-type', 'Unknown')}")
                
                if response.status_code == 200:
                    print("   ✅ SUCCESS!")
                    try:
                        # Try to parse as JSON
                        data = response.json()
                        print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
                    except:
                        # If not JSON, show first 200 chars
                        print(f"   Response: {response.text[:200]}...")
                elif response.status_code == 404:
                    print("   ❌ Not Found")
                elif response.status_code == 405:
                    print("   ❌ Method Not Allowed (try POST instead of GET)")
                else:
                    print(f"   ❌ Error: {response.status_code}")
                    print(f"   Response: {response.text[:200]}...")
                
                print()
                
            except requests.exceptions.Timeout:
                print(f"   ❌ Timeout")
                print()
            except Exception as e:
                print(f"   ❌ Error: {e}")
                print()
        
        # Test POST endpoints for chat
        print("🔍 Testing POST endpoints for chat...")
        print()
        
        post_endpoints = [
            "/chat/completions",
            "/v1/chat/completions", 
            "/api/chat/completions",
            "/completions",
            "/v1/completions"
        ]
        
        test_payload = {
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10
        }
        
        for endpoint in post_endpoints:
            try:
                url = f"{client.base_url}{endpoint}"
                print(f"🔧 Testing POST: {endpoint}")
                
                response = requests.post(url, headers=headers, json=test_payload, timeout=10)
                
                print(f"   Status: {response.status_code}")
                print(f"   Content-Type: {response.headers.get('content-type', 'Unknown')}")
                
                if response.status_code == 200:
                    print("   ✅ SUCCESS!")
                    try:
                        data = response.json()
                        print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
                    except:
                        print(f"   Response: {response.text[:200]}...")
                else:
                    print(f"   ❌ Error: {response.status_code}")
                    print(f"   Response: {response.text[:200]}...")
                
                print()
                
            except requests.exceptions.Timeout:
                print(f"   ❌ Timeout")
                print()
            except Exception as e:
                print(f"   ❌ Error: {e}")
                print()
                
    except Exception as e:
        print(f"❌ Error initializing client: {e}")

def main():
    debug_service_endpoints()
    
    print("=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    print("💡 Look for endpoints that return:")
    print("   - Status 200 with JSON response")
    print("   - Models endpoint that lists available models")
    print("   - Chat endpoint that accepts POST requests")
    print()
    print("💡 Update your llama_client.py with the correct endpoints")

if __name__ == "__main__":
    main() 