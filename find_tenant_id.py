#!/usr/bin/env python3
"""
Script to help find the correct tenant ID for Munich Re organization
"""

import requests
import json
from config import CLIENT_ID, CLIENT_SECRET, AUTH_URI

def discover_tenant_id():
    """Try to discover the tenant ID using the client ID"""
    try:
        # Try to get tenant information using the client ID
        url = f"{AUTH_URI}/common/discovery/instance"
        params = {
            "api-version": "1.0",
            "client_id": CLIENT_ID
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Successfully discovered tenant information:")
            print(f"   Tenant ID: {data.get('tenant_id', 'Not found')}")
            print(f"   Tenant Name: {data.get('tenant_name', 'Not found')}")
            return data.get('tenant_id')
        else:
            print(f"❌ Failed to discover tenant: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error discovering tenant: {e}")
        return None

def test_known_tenant_ids():
    """Test common tenant ID patterns for Munich Re"""
    
    # Common patterns for Munich Re
    tenant_patterns = [
        "munichre.onmicrosoft.com",
        "munichre.com",
        "munich-re.com",
        "munichre",
        "munich-re"
    ]
    
    print("🔍 Testing common tenant ID patterns for Munich Re...")
    print("=" * 50)
    
    for pattern in tenant_patterns:
        try:
            # Test if this tenant exists
            url = f"{AUTH_URI}/{pattern}/.well-known/openid_configuration"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Found valid tenant: {pattern}")
                return pattern
            else:
                print(f"❌ Invalid tenant: {pattern}")
                
        except Exception as e:
            print(f"❌ Error testing {pattern}: {e}")
    
    return None

def main():
    print("🔍 Munich Re Tenant ID Discovery")
    print("=" * 50)
    
    print("1. Trying to discover tenant ID automatically...")
    tenant_id = discover_tenant_id()
    
    if not tenant_id:
        print("\n2. Trying common tenant ID patterns...")
        tenant_id = test_known_tenant_ids()
    
    if tenant_id:
        print(f"\n✅ Found tenant ID: {tenant_id}")
        print("\n💡 Update your config.py with:")
        print(f"   TENANT_ID = \"{tenant_id}\"")
        print("\nThen try the authentication again.")
    else:
        print("\n❌ Could not automatically discover tenant ID.")
        print("\n💡 Manual steps to find your tenant ID:")
        print("   1. Ask your Azure administrator")
        print("   2. Check Azure Portal: Azure Active Directory → Overview → Tenant ID")
        print("   3. Use PowerShell: Get-AzureADTenantDetail")
        print("   4. Check your organization's documentation")

if __name__ == "__main__":
    main() 