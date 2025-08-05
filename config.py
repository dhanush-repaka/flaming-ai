import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LLAMA LLM Configuration
CLIENT_ID = "dc1d7b7c-e795-43b9-984d-0f2737e7a3211"
CLIENT_SECRET = "HQt8Q~Mq2ihqcPnjzA5lP4H06kb551i~EF40nbYF"
APIM_SUBSCRIPTION_KEY = "5e132f1fe1bd4bcba225867ef9fb53f81"
BASE_URL = "https://prdus-gateway-llm-large.app-prd-eus-204.k8s.munichre.com"
AUTH_URI = "https://login.microsoftonline.com"

# Azure AD Configuration
TENANT_ID = "common"  # You may need to update this with your specific tenant ID
SCOPE = ["https://graph.microsoft.com/.default"]  # Adjust scope as needed 