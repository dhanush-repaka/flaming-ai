#!/usr/bin/env python3
"""
Discover the correct API endpoint and configuration
"""

import requests
import json
from config import BASE_URL, CLIENT_ID, CLIENT_SECRET, APIM_SUBSCRIPTION_KEY

def discover_api_endpoints():
    """Try to discover the correct API endpoints"""
    print("🔍 Discovering API Endpoints")
    print("=" * 50)
    
    # Try different base URL patterns
    base_urls_to_test = [
        BASE_URL,
        BASE_URL.replace("https://", "https://api."),
        BASE_URL.replace("https://", "https://gateway."),
        BASE_URL.replace("https://", "https://llm."),
        BASE_URL.replace("https://", "https://llama."),
        BASE_URL.replace("gateway-llm-large", "llm"),
        BASE_URL.replace("gateway-llm-large", "llama"),
        BASE_URL.replace("gateway-llm-large", "api"),
    ]
    
    # Try different path patterns
    path_patterns = [
        "/api/v1",
        "/v1",
        "/api",
        "/llm",
        "/llama",
        "/chat",
        "/openai",
        "/completions"
    ]
    
    print("Testing different base URLs and paths...")
    print()
    
    for base_url in base_urls_to_test:
        print(f"🔧 Testing base URL: {base_url}")
        print("-" * 40)
        
        for path in path_patterns:
            try:
                url = f"{base_url}{path}/models"
                
                # Try with subscription key only first
                headers = {
                    "Ocp-Apim-Subscription-Key": APIM_SUBSCRIPTION_KEY,
                    "Content-Type": "application/json"
                }
                
                response = requests.get(url, headers=headers, timeout=10)
                
                print(f"   {path}/models: Status {response.status_code}")
                
                if response.status_code == 200:
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
                            print("   ❌ Login page")
                        else:
                            print("   ⚠️  HTML (not login page)")
                    else:
                        print(f"   Response: {response.text[:100]}...")
                elif response.status_code == 401:
                    print("   ❌ Unauthorized")
                elif response.status_code == 404:
                    print("   ❌ Not Found")
                else:
                    print(f"   ❌ Error: {response.status_code}")
                
                print()
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                print()
        
        print()

def test_different_auth_methods():
    """Test different authentication methods"""
    print("🔍 Testing Different Authentication Methods")
    print("=" * 50)
    
    # Try the original URL with different auth methods
    url = f"{BASE_URL}/models"
    
    auth_methods = [
        {
            "name": "No Auth",
            "headers": {"Content-Type": "application/json"}
        },
        {
            "name": "Subscription Key Only",
            "headers": {
                "Ocp-Apim-Subscription-Key": APIM_SUBSCRIPTION_KEY,
                "Content-Type": "application/json"
            }
        },
        {
            "name": "API Key Header",
            "headers": {
                "X-API-Key": APIM_SUBSCRIPTION_KEY,
                "Content-Type": "application/json"
            }
        },
        {
            "name": "Authorization Header",
            "headers": {
                "Authorization": f"Bearer {APIM_SUBSCRIPTION_KEY}",
                "Content-Type": "application/json"
            }
        }
    ]
    
    for method in auth_methods:
        try:
            print(f"🔧 Testing: {method['name']}")
            response = requests.get(url, headers=method["headers"], timeout=10)
            
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'Unknown')}")
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'application/json' in content_type:
                    print("   ✅ JSON Response!")
                elif 'text/html' in content_type:
                    if 'Sign in to your account' in response.text:
                        print("   ❌ Login page")
                    else:
                        print("   ⚠️  HTML (not login page)")
                else:
                    print(f"   Response: {response.text[:100]}...")
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   Response: {response.text[:100]}...")
            
            print()
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print()

def main():
    discover_api_endpoints()
    test_different_auth_methods()
    
    print("=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    print("💡 If no JSON responses found, you may need to:")
    print("   1. Ask your Azure administrator for the correct API endpoint")
    print("   2. Check if the service requires different authentication")
    print("   3. Verify the API gateway configuration")
    print("   4. Check if there's a different service URL")

if __name__ == "__main__":
    main() 