import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LLAMA LLM Configuration
CLIENT_ID = "dc1d7b7c-e795-43b9-984d-0f2737e7a321"
CLIENT_SECRET = "HQt8Q~Mq2ihqcPnjzA5lP4H06kb551i~EF40nbYF"
APIM_SUBSCRIPTION_KEY = "5e132f1fe1bd4bcba225867ef9fb53f8"
BASE_URL = "https://prdus-gateway-llm-large.app-prd-eus-204.k8s.munichre.com"
AUTH_URI = "https://login.microsoftonline.com"

# Azure AD Configuration
TENANT_ID = "munichre.onmicrosoft.com"  # Munich Re tenant ID
# Try different scope options - uncomment the one that works for your service
SCOPE = [".default"]  # Option 1: Default scope (try this first)
# SCOPE = ["https://prdus-gateway-llm-large.app-prd-eus-204.k8s.munichre.com/.default"]  # Option 2: Full base URL
# SCOPE = ["https://prdus-gateway-llm-large/.default"]  # Option 3: Simplified
# SCOPE = ["https://k8s.munichre.com/.default"]  # Option 4: Domain only
# SCOPE = ["https://graph.microsoft.com/.default"]  # Option 5: Microsoft Graph (original)
# SCOPE = []  # Option 6: No scope (doesn't work with Azure AD) 