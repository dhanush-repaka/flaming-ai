# LLAMA LLM Client

A Python client for connecting to and chatting with LLAMA LLM hosted on the Flamingo server.

## Features

- 🔐 **Secure Authentication**: Uses Azure AD client credentials flow
- 🧪 **Connection Testing**: Built-in connection testing functionality
- 💬 **Interactive Chat**: Modern web-based chat interface
- 📊 **Model Information**: Get available models from the service
- 📥 **Chat Export**: Export chat conversations to JSON
- 🔧 **Configurable**: Easy configuration management
- 🎨 **Modern UI**: Beautiful, responsive frontend design
- 📱 **Real-time Chat**: Live chat with typing indicators
- 📈 **Chat Statistics**: Track message counts and usage

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configuration

The application is pre-configured with your provided credentials:

- **Client ID**: `dc1d7b7c-e795-43b9-984d-0f2737e7a3211`
- **Client Secret**: `HQt8Q~Mq2ihqcPnjzA5lP4H06kb551i~EF40nbYF`
- **APIM Subscription Key**: `5e132f1fe1bd4bcba225867ef9fb53f81`
- **Base URL**: `https://prdus-gateway-llm-large.app-prd-eus-204.k8s.munichre.com`
- **Auth URI**: `https://login.microsoftonline.com`

## Usage

### 1. Test Connection

First, test the connection to ensure everything is working:

```bash
python test_connection.py
```

This will:
- Test authentication
- Test service connectivity
- Check available models
- Test chat functionality

### 2. Start Chat Application

#### Option A: Modern Web Interface (Recommended)

Launch the Flask backend with modern frontend:

```bash
python start_server.py
```

Then choose option 1 to start the Flask backend. The application will be available at `http://localhost:5000`.

#### Option B: Streamlit Interface

Launch the Streamlit chat interface:

```bash
streamlit run chat_app.py
```

The application will open in your browser at `http://localhost:8501`.

### 3. Programmatic Usage

You can also use the client programmatically:

```python
from llama_client import LlamaClient

# Initialize client
client = LlamaClient()

# Test connection
result = client.test_connection()
print(result)

# Send a chat message
response = client.send_chat_message("Hello, how are you?")
print(response["message"])

# Get available models
models = client.get_available_models()
print(models)
```

## API Endpoints

The client supports the following operations:

### Authentication
- **Method**: `get_access_token()`
- **Description**: Obtains access token using client credentials flow
- **Returns**: Access token string

### Connection Testing
- **Method**: `test_connection()`
- **Description**: Tests connectivity to the LLAMA service
- **Returns**: Dictionary with status and response

### Chat
- **Method**: `send_chat_message(message, conversation_history=None)`
- **Description**: Sends a message to the LLAMA LLM
- **Parameters**:
  - `message`: The message to send
  - `conversation_history`: Optional list of previous messages
- **Returns**: Dictionary with status and response

### Models
- **Method**: `get_available_models()`
- **Description**: Gets list of available models
- **Returns**: Dictionary with status and models data

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify your client ID and secret are correct
   - Check if your Azure AD app has the necessary permissions
   - Ensure the tenant ID is correct

2. **Connection Failed**
   - Verify the base URL is correct
   - Check if the service is accessible from your network
   - Ensure the subscription key is valid

3. **Chat Endpoint Not Found**
   - The service might use different endpoint paths
   - Check the actual API documentation for the correct endpoints
   - Update the endpoint URLs in `llama_client.py`

### Debug Mode

To enable debug logging, add this to your script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## File Structure

```
flaming-ai/
├── config.py              # Configuration settings
├── llama_client.py        # Main LLAMA client class
├── test_connection.py     # Connection testing script
├── chat_app.py           # Streamlit web application
├── app.py                # Flask backend server
├── start_server.py       # Startup script with options
├── requirements.txt       # Python dependencies
├── frontend/             # Modern web frontend
│   ├── index.html        # Main HTML file
│   ├── styles.css        # CSS styles
│   └── script.js         # JavaScript functionality
└── README.md             # This file
```

## Security Notes

- Credentials are stored in the `config.py` file
- In production, consider using environment variables
- The access token is automatically refreshed when needed
- All API calls use HTTPS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for internal use with the Flamingo LLAMA LLM service. 