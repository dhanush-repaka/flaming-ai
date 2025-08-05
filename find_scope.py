#!/usr/bin/env python3
"""
Diagnostic script to help find the correct scope and tenant ID for Azure AD authentication
"""

import msal
import requests
from config import CLIENT_ID, CLIENT_SECRET, AUTH_URI

def test_authentication_with_scope(scope, tenant_id="common"):
    """Test authentication with a specific scope and tenant ID"""
    try:
        app = msal.ConfidentialClientApplication(
            client_id=CLIENT_ID,
            client_credential=CLIENT_SECRET,
            authority=f"{AUTH_URI}/{tenant_id}"
        )
        
        result = app.acquire_token_for_client(scopes=[scope])
        
        if "access_token" in result:
            return True, "Success", result.get("access_token", "")[:50] + "..."
        else:
            return False, result.get('error_description', 'Unknown error'), None
            
    except Exception as e:
        return False, str(e), None

def main():
    print("🔍 Azure AD Scope and Tenant ID Diagnostic")
    print("=" * 50)
    
    # Common scope patterns to try
    scopes_to_test = [
        ".default",
        "https://graph.microsoft.com/.default",
        "https://prdus-gateway-llm-large.app-prd-eus-204.k8s.munichre.com/.default",
        "https://prdus-gateway-llm-large/.default",
        "https://k8s.munichre.com/.default",
        "https://munichre.com/.default",
        "https://api.azure.com/.default",
        "https://management.azure.com/.default"
    ]
    
    # Common tenant IDs to try
    tenant_ids_to_test = [
        "common",
        "organizations",
        "consumers"
    ]
    
    print("Testing different scope and tenant ID combinations...")
    print()
    
    successful_combinations = []
    
    for tenant_id in tenant_ids_to_test:
        print(f"🔧 Testing with Tenant ID: {tenant_id}")
        print("-" * 30)
        
        for scope in scopes_to_test:
            success, message, token_preview = test_authentication_with_scope(scope, tenant_id)
            
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"{status} | Scope: {scope}")
            print(f"   Message: {message}")
            if token_preview:
                print(f"   Token: {token_preview}")
            print()
            
            if success:
                successful_combinations.append((scope, tenant_id, message))
    
    print("=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    
    if successful_combinations:
        print("✅ Successful combinations found:")
        for scope, tenant_id, message in successful_combinations:
            print(f"   - Scope: {scope}")
            print(f"   - Tenant ID: {tenant_id}")
            print(f"   - Message: {message}")
            print()
        
        print("💡 To use the first successful combination, update your config.py:")
        first_scope, first_tenant, _ = successful_combinations[0]
        print(f"   SCOPE = [\"{first_scope}\"]")
        print(f"   TENANT_ID = \"{first_tenant}\"")
    else:
        print("❌ No successful combinations found.")
        print()
        print("💡 Next steps:")
        print("   1. Check with your Azure administrator for the correct scope")
        print("   2. Verify your CLIENT_ID and CLIENT_SECRET are correct")
        print("   3. Ensure your app registration has the necessary permissions")
        print("   4. Check if Conditional Access policies are blocking access")

if __name__ == "__main__":
    main() 