#!/usr/bin/env python3
"""
Simple network connectivity test for the LLAMA service
"""

import requests
import socket
from config import BASE_URL

def test_basic_connectivity():
    """Test basic network connectivity"""
    print("🔍 Testing Network Connectivity")
    print("=" * 50)
    
    # Extract hostname from URL
    hostname = BASE_URL.replace("https://", "").replace("http://", "")
    
    print(f"Testing connectivity to: {hostname}")
    print()
    
    # Test 1: DNS resolution
    try:
        ip = socket.gethostbyname(hostname)
        print(f"✅ DNS Resolution: {hostname} → {ip}")
    except socket.gaierror as e:
        print(f"❌ DNS Resolution failed: {e}")
        return False
    
    # Test 2: Basic HTTP connection
    try:
        response = requests.get(f"https://{hostname}", timeout=10, verify=True)
        print(f"✅ HTTP Connection: Status {response.status_code}")
    except requests.exceptions.SSLError as e:
        print(f"⚠️  SSL Certificate issue: {e}")
        print("   This might be expected for internal services")
    except requests.exceptions.ConnectTimeout as e:
        print(f"❌ Connection timeout: {e}")
        return False
    except requests.exceptions.ReadTimeout as e:
        print(f"❌ Read timeout: {e}")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    # Test 3: Try different endpoints
    endpoints_to_test = [
        "/",
        "/health",
        "/status",
        "/ping",
        "/api/health",
        "/v1/health"
    ]
    
    print("\n🔍 Testing different endpoints:")
    for endpoint in endpoints_to_test:
        try:
            url = f"https://{hostname}{endpoint}"
            response = requests.get(url, timeout=5, verify=False)
            print(f"✅ {endpoint}: Status {response.status_code}")
        except requests.exceptions.SSLError:
            print(f"⚠️  {endpoint}: SSL Certificate issue")
        except requests.exceptions.Timeout:
            print(f"❌ {endpoint}: Timeout")
        except requests.exceptions.ConnectionError:
            print(f"❌ {endpoint}: Connection error")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")
    
    return True

def main():
    print("🌐 LLAMA Service Network Test")
    print("=" * 50)
    
    success = test_basic_connectivity()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Basic connectivity test completed")
        print("💡 If you're still getting timeouts, it might be:")
        print("   1. VPN requirement")
        print("   2. Internal network access needed")
        print("   3. Firewall restrictions")
        print("   4. Service is down or misconfigured")
    else:
        print("❌ Network connectivity issues detected")
        print("💡 Check your network connection and VPN status")

if __name__ == "__main__":
    main() 