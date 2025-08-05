#!/usr/bin/env python3
"""
Try common tenant ID patterns for Munich Re
"""

import msal
from config import CLIENT_ID, CLIENT_SECRET, AUTH_URI

def test_tenant_pattern(pattern):
    """Test if a tenant pattern is valid"""
    try:
        app = msal.ConfidentialClientApplication(
            client_id=CLIENT_ID,
            client_credential=CLIENT_SECRET,
            authority=f"{AUTH_URI}/{pattern}"
        )
        
        # Try to get a token with a simple scope
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        
        if "access_token" in result:
            return True, "✅ SUCCESS - Found valid tenant!"
        else:
            error = result.get('error_description', 'Unknown error')
            if "AADSTS500011" in error:
                return False, "❌ Resource not found in this tenant"
            elif "AADSTS700016" in error:
                return False, "❌ App not found in this tenant"
            else:
                return False, f"❌ {error}"
                
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def main():
    print("🔍 Testing Munich Re Tenant ID Patterns")
    print("=" * 50)
    
    # Common patterns for Munich Re (based on typical corporate patterns)
    patterns_to_test = [
        # Common corporate patterns
        "munichre.onmicrosoft.com",
        "munich-re.onmicrosoft.com",
        "munichre.com",
        "munich-re.com",
        
        # Possible tenant IDs (you might know these)
        "munichre",
        "munich-re",
        "munichreinsurance",
        "munichreinsurance.com",
        
        # Try some common GUID patterns (replace with actual ones if you know them)
        # "12345678-1234-1234-1234-123456789012",  # Example GUID
    ]
    
    print("Testing tenant patterns...")
    print()
    
    valid_tenants = []
    
    for pattern in patterns_to_test:
        print(f"🔧 Testing: {pattern}")
        success, message = test_tenant_pattern(pattern)
        print(f"   {message}")
        print()
        
        if success:
            valid_tenants.append(pattern)
    
    print("=" * 50)
    print("📋 RESULTS")
    print("=" * 50)
    
    if valid_tenants:
        print("✅ Valid tenants found:")
        for tenant in valid_tenants:
            print(f"   - {tenant}")
        print()
        print("💡 Update your config.py with:")
        print(f"   TENANT_ID = \"{valid_tenants[0]}\"")
    else:
        print("❌ No valid tenant patterns found.")
        print()
        print("💡 You need to find your specific tenant ID:")
        print("   1. Ask your Azure administrator")
        print("   2. Check Azure Portal: Azure Active Directory → Overview → Tenant ID")
        print("   3. Look in your organization's documentation")
        print("   4. Check if you have access to Azure CLI: az account show")

if __name__ == "__main__":
    main() 