#!/usr/bin/env python3
"""
Test different authentication header combinations
"""

import requests
import json
from llama_client import LlamaClient

def test_auth_headers():
    """Test different authentication header combinations"""
    print("🔍 Testing Authentication Headers")
    print("=" * 50)
    
    try:
        # Initialize client
        client = LlamaClient()
        client.ensure_valid_token()
        
        # Different header combinations to try
        header_combinations = [
            {
                "name": "Bearer + Subscription Key",
                "headers": {
                    "Authorization": f"Bearer {client.access_token}",
                    "Ocp-Apim-Subscription-Key": client.subscription_key,
                    "Content-Type": "application/json"
                }
            },
            {
                "name": "Bearer Only",
                "headers": {
                    "Authorization": f"Bearer {client.access_token}",
                    "Content-Type": "application/json"
                }
            },
            {
                "name": "Subscription Key Only",
                "headers": {
                    "Ocp-Apim-Subscription-Key": client.subscription_key,
                    "Content-Type": "application/json"
                }
            },
            {
                "name": "API Key Header",
                "headers": {
                    "X-API-Key": client.subscription_key,
                    "Content-Type": "application/json"
                }
            },
            {
                "name": "Authorization Header Only",
                "headers": {
                    "Authorization": f"Bearer {client.access_token}"
                }
            },
            {
                "name": "Custom Auth Header",
                "headers": {
                    "X-Auth-Token": client.access_token,
                    "Ocp-Apim-Subscription-Key": client.subscription_key,
                    "Content-Type": "application/json"
                }
            }
        ]
        
        # Test endpoints
        test_endpoints = ["/models", "/chat/completions"]
        
        for combo in header_combinations:
            print(f"\n🔧 Testing: {combo['name']}")
            print("-" * 30)
            
            for endpoint in test_endpoints:
                try:
                    url = f"{client.base_url}{endpoint}"
                    
                    if endpoint == "/chat/completions":
                        # Use POST for chat endpoint
                        payload = {"messages": [{"role": "user", "content": "Hello"}], "max_tokens": 10}
                        response = requests.post(url, headers=combo["headers"], json=payload, timeout=10)
                    else:
                        # Use GET for models endpoint
                        response = requests.get(url, headers=combo["headers"], timeout=10)
                    
                    print(f"   {endpoint}: Status {response.status_code}")
                    print(f"   Content-Type: {response.headers.get('content-type', 'Unknown')}")
                    
                    if response.status_code == 200:
                        # Check if it's JSON or HTML
                        content_type = response.headers.get('content-type', '')
                        if 'application/json' in content_type:
                            print("   ✅ JSON Response!")
                            try:
                                data = response.json()
                                print(f"   Response: {json.dumps(data, indent=2)[:200]}...")
                            except:
                                print("   Response: Could not parse JSON")
                        elif 'text/html' in content_type:
                            if 'Sign in to your account' in response.text:
                                print("   ❌ Still getting login page")
                            else:
                                print("   ⚠️  HTML response (not login page)")
                        else:
                            print(f"   Response: {response.text[:100]}...")
                    else:
                        print(f"   ❌ Error: {response.status_code}")
                        print(f"   Response: {response.text[:100]}...")
                    
                    print()
                    
                except Exception as e:
                    print(f"   ❌ Error: {e}")
                    print()
        
    except Exception as e:
        print(f"❌ Error initializing client: {e}")

def main():
    test_auth_headers()
    
    print("=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    print("💡 Look for:")
    print("   - JSON responses instead of HTML")
    print("   - No 'Sign in to your account' messages")
    print("   - Proper API responses")
    print()
    print("💡 If all still return HTML, the service might need:")
    print("   - Different authentication method")
    print("   - Additional headers")
    print("   - Different API gateway configuration")

if __name__ == "__main__":
    main() 