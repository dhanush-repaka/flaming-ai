#!/usr/bin/env python3
"""
Startup script for LLAMA LLM Chat Application
"""

import sys
import subprocess
import os

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🤖 LLAMA LLM Chat Application")
    print("=" * 60)
    print()

def print_options():
    """Print available options"""
    print("Choose an option:")
    print("1. 🚀 Start Flask Backend (Recommended)")
    print("   - Modern web interface")
    print("   - Connection testing first")
    print("   - Real-time chat")
    print("   - Available at: http://localhost:5000")
    print()
    print("2. 📱 Start Streamlit App")
    print("   - Alternative interface")
    print("   - Available at: http://localhost:8501")
    print()
    print("3. 🧪 Test Connection Only")
    print("   - Quick connection test")
    print("   - No web interface")
    print()
    print("4. 📋 Show Configuration")
    print("   - Display current settings")
    print()
    print("0. ❌ Exit")
    print()

def start_flask_backend():
    """Start the Flask backend server"""
    print("🚀 Starting Flask Backend Server...")
    print("📱 Frontend will be available at: http://localhost:5000")
    print("🔧 API endpoints:")
    print("   - POST /api/test-connection")
    print("   - POST /api/chat")
    print("   - GET  /api/models")
    print("   - GET  /api/health")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def start_streamlit_app():
    """Start the Streamlit app"""
    print("📱 Starting Streamlit App...")
    print("🌐 App will be available at: http://localhost:8501")
    print()
    print("Press Ctrl+C to stop the app")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "chat_app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error starting app: {e}")

def test_connection():
    """Run connection test"""
    print("🧪 Testing LLAMA LLM Connection...")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, "test_connection.py"], check=True)
    except Exception as e:
        print(f"❌ Error running test: {e}")

def show_configuration():
    """Show current configuration"""
    print("📋 Current Configuration")
    print("=" * 50)
    
    try:
        from config import CLIENT_ID, CLIENT_SECRET, APIM_SUBSCRIPTION_KEY, BASE_URL, AUTH_URI
        
        print(f"Client ID: {CLIENT_ID}")
        print(f"Client Secret: {'*' * len(CLIENT_SECRET)}")
        print(f"APIM Subscription Key: {'*' * len(APIM_SUBSCRIPTION_KEY)}")
        print(f"Base URL: {BASE_URL}")
        print(f"Auth URI: {AUTH_URI}")
        print()
        print("✅ Configuration loaded successfully")
        
    except ImportError as e:
        print(f"❌ Error loading configuration: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Define package names and their corresponding import names
    package_imports = {
        'requests': 'requests',
        'msal': 'msal', 
        'python-dotenv': 'dotenv',  # python-dotenv installs as 'dotenv'
        'streamlit': 'streamlit',
        'flask': 'flask',
        'flask-cors': 'flask_cors'
    }
    
    missing_packages = []
    
    for package, import_name in package_imports.items():
        try:
            __import__(import_name)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print()
        print("⚠️  Missing dependencies detected!")
        print("Please install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        print()
        return False
    
    print("✅ All dependencies are installed!")
    print()
    return True

def main():
    """Main function"""
    print_banner()
    
    # Check dependencies first
    if not check_dependencies():
        print("Please install missing dependencies and try again.")
        return
    
    while True:
        print_options()
        
        try:
            choice = input("Enter your choice (0-4): ").strip()
            
            if choice == "1":
                start_flask_backend()
                break
            elif choice == "2":
                start_streamlit_app()
                break
            elif choice == "3":
                test_connection()
                break
            elif choice == "4":
                show_configuration()
                input("\nPress Enter to continue...")
            elif choice == "0":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 0-4.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main() 