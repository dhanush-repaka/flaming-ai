#!/usr/bin/env python3
"""
Simple test to get more information about the service
"""

import requests
from config import BASE_URL, APIM_SUBSCRIPTION_KEY

def simple_test():
    """Simple test to understand the service better"""
    print("🔍 Simple Service Test")
    print("=" * 50)
    
    # Test 1: Basic connectivity without auth
    print("1. Testing basic connectivity...")
    try:
        response = requests.get(BASE_URL, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type', 'Unknown')}")
        print(f"   Response length: {len(response.text)} characters")
        if len(response.text) < 500:
            print(f"   Response: {response.text}")
        else:
            print(f"   Response preview: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 2: Check response headers
    print("2. Checking response headers...")
    try:
        response = requests.get(BASE_URL, timeout=10)
        print("   Headers:")
        for key, value in response.headers.items():
            print(f"     {key}: {value}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 3: Try with subscription key
    print("3. Testing with subscription key...")
    try:
        headers = {"Ocp-Apim-Subscription-Key": APIM_SUBSCRIPTION_KEY}
        response = requests.get(BASE_URL, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type', 'Unknown')}")
        if response.status_code != 200:
            print(f"   Error response: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 4: Check if there's an API documentation endpoint
    print("4. Checking for API documentation...")
    doc_endpoints = ["/swagger", "/docs", "/api-docs", "/openapi.json", "/swagger.json"]
    for endpoint in doc_endpoints:
        try:
            url = f"{BASE_URL}{endpoint}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ Found: {endpoint}")
                print(f"   Content-Type: {response.headers.get('content-type', 'Unknown')}")
            else:
                print(f"   ❌ Not found: {endpoint}")
        except:
            print(f"   ❌ Error: {endpoint}")

def main():
    simple_test()
    
    print("\n" + "=" * 50)
    print("📋 NEXT STEPS")
    print("=" * 50)
    print("💡 Based on the results:")
    print("   1. If you see API documentation, check the correct endpoints")
    print("   2. If you see error messages, they might give clues")
    print("   3. Contact your Azure administrator for the correct configuration")
    print("   4. Check if there's a different service URL or authentication method")

if __name__ == "__main__":
    main() 