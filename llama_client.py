import requests
import msal
import json
import time
from typing import Dict, List, Optional
from config import CLIENT_ID, CLIENT_SECRET, APIM_SUBSCRIPTION_KEY, BASE_URL, AUTH_URI, TENANT_ID, SCOPE


class LlamaClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.subscription_key = APIM_SUBSCRIPTION_KEY
        self.auth_uri = AUTH_URI
        self.tenant_id = TENANT_ID
        self.scope = SCOPE
        self.access_token = None
        self.token_expires_at = 0
        
    def get_access_token(self) -> str:
        """Get access token using client credentials flow"""
        try:
            # Create MSAL application
            app = msal.ConfidentialClientApplication(
                client_id=self.client_id,
                client_credential=self.client_secret,
                authority=f"{self.auth_uri}/{self.tenant_id}"
            )
            
            # Get token
            result = app.acquire_token_for_client(scopes=self.scope)
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                # Set expiration time (subtract 5 minutes for safety)
                self.token_expires_at = time.time() + result.get("expires_in", 3600) - 300
                return self.access_token
            else:
                raise Exception(f"Failed to get access token: {result.get('error_description', 'Unknown error')}")
                
        except Exception as e:
            raise Exception(f"Authentication failed: {str(e)}")
    
    def is_token_valid(self) -> bool:
        """Check if current token is still valid"""
        return self.access_token and time.time() < self.token_expires_at
    
    def ensure_valid_token(self):
        """Ensure we have a valid access token"""
        if not self.is_token_valid():
            self.get_access_token()
    
    def test_connection(self) -> Dict:
        """Test the connection to the LLAMA LLM service"""
        try:
            self.ensure_valid_token()
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Ocp-Apim-Subscription-Key": self.subscription_key,
                "Content-Type": "application/json"
            }
            
            # Test endpoint - you may need to adjust this based on the actual API
            test_url = f"{self.base_url}/health"  # or /status, /ping, etc.
            
            response = requests.get(test_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "Connection successful",
                    "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                }
            else:
                return {
                    "status": "error",
                    "message": f"Connection failed with status {response.status_code}",
                    "response": response.text
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Network error: {str(e)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }
    
    def send_chat_message(self, message: str, conversation_history: Optional[List[Dict]] = None) -> Dict:
        """Send a chat message to the LLAMA LLM"""
        try:
            self.ensure_valid_token()
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Ocp-Apim-Subscription-Key": self.subscription_key,
                "Content-Type": "application/json"
            }
            
            # Prepare the request payload
            payload = {
                "messages": conversation_history or [],
                "max_tokens": 1000,
                "temperature": 0.7,
                "top_p": 0.9,
                "frequency_penalty": 0,
                "presence_penalty": 0
            }
            
            # Add the new message
            payload["messages"].append({
                "role": "user",
                "content": message
            })
            
            # Send request to chat endpoint
            chat_url = f"{self.base_url}/chat/completions"  # Adjust endpoint as needed
            
            response = requests.post(chat_url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                response_data = response.json()
                return {
                    "status": "success",
                    "response": response_data,
                    "message": response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
                }
            else:
                return {
                    "status": "error",
                    "message": f"Chat request failed with status {response.status_code}",
                    "response": response.text
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Network error: {str(e)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }
    
    def get_available_models(self) -> Dict:
        """Get list of available models"""
        try:
            self.ensure_valid_token()
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Ocp-Apim-Subscription-Key": self.subscription_key,
                "Content-Type": "application/json"
            }
            
            models_url = f"{self.base_url}/models"
            
            response = requests.get(models_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "models": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to get models with status {response.status_code}",
                    "response": response.text
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error getting models: {str(e)}"
            } 