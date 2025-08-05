#!/usr/bin/env python3
"""
Flask backend server for LLAMA LLM Chat Interface
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from llama_client import LlamaClient

app = Flask(__name__)
CORS(app)

# Global client instance
llama_client = None

def get_llama_client():
    """Get or create LLAMA client instance"""
    global llama_client
    if llama_client is None:
        llama_client = LlamaClient()
    return llama_client

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files from frontend directory"""
    return send_from_directory('frontend', filename)

@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    """Test connection to LLAMA LLM service"""
    try:
        client = get_llama_client()
        result = client.test_connection()
        
        if result["status"] == "success":
            return jsonify({
                "status": "success",
                "message": "Connection successful!",
                "details": "All services are operational"
            })
        else:
            return jsonify({
                "status": "error",
                "message": result["message"],
                "details": "Please check your configuration and network connection"
            })
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Connection test failed: {str(e)}",
            "details": "Check server logs for more information"
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Send a chat message to LLAMA LLM"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        conversation_history = data.get('conversation_history', [])
        
        if not message:
            return jsonify({
                "status": "error",
                "message": "Message cannot be empty"
            }), 400
        
        client = get_llama_client()
        result = client.send_chat_message(message, conversation_history)
        
        if result["status"] == "success":
            return jsonify({
                "status": "success",
                "message": result["message"]
            })
        else:
            return jsonify({
                "status": "error",
                "message": result["message"]
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Chat request failed: {str(e)}"
        }), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available models from LLAMA LLM service"""
    try:
        client = get_llama_client()
        result = client.get_available_models()
        
        if result["status"] == "success":
            return jsonify({
                "status": "success",
                "models": result["models"]
            })
        else:
            return jsonify({
                "status": "error",
                "message": result["message"]
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to get models: {str(e)}"
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "LLAMA LLM Chat Backend",
        "version": "1.0.0"
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    print("🚀 Starting LLAMA LLM Chat Server...")
    print("📱 Frontend will be available at: http://localhost:5000")
    print("🔧 API endpoints:")
    print("   - POST /api/test-connection")
    print("   - POST /api/chat")
    print("   - GET  /api/models")
    print("   - GET  /api/health")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 