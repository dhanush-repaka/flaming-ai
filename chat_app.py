#!/usr/bin/env python3
"""
Streamlit Chat Application for LLAMA LLM
"""

import streamlit as st
import json
from llama_client import LlamaClient

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "client" not in st.session_state:
        st.session_state.client = None
    if "connection_status" not in st.session_state:
        st.session_state.connection_status = "not_tested"

def test_connection():
    """Test connection to LLAMA LLM"""
    try:
        client = LlamaClient()
        result = client.test_connection()
        
        if result["status"] == "success":
            st.session_state.connection_status = "connected"
            st.session_state.client = client
            return True, "Connection successful!"
        else:
            st.session_state.connection_status = "failed"
            return False, f"Connection failed: {result['message']}"
    except Exception as e:
        st.session_state.connection_status = "failed"
        return False, f"Error: {str(e)}"

def send_message(message):
    """Send a message to the LLAMA LLM"""
    if not st.session_state.client:
        return "Error: No connection to LLAMA LLM"
    
    try:
        # Convert session messages to the format expected by the API
        conversation_history = []
        for msg in st.session_state.messages:
            conversation_history.append({
                "role": "user" if msg["role"] == "user" else "assistant",
                "content": msg["content"]
            })
        
        result = st.session_state.client.send_chat_message(message, conversation_history)
        
        if result["status"] == "success":
            return result["message"]
        else:
            return f"Error: {result['message']}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.set_page_config(
        page_title="LLAMA LLM Chat",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 LLAMA LLM Chat Interface")
    st.markdown("---")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar for all controls and info
    with st.sidebar:
        st.header("🔧 Connection & Settings")
        
        # Connection status
        if st.session_state.connection_status == "connected":
            st.success("✅ Connected to LLAMA LLM")
        elif st.session_state.connection_status == "failed":
            st.error("❌ Connection failed")
        else:
            st.info("⏳ Connection not tested")
        
        # Test connection button
        if st.button("🔗 Test Connection"):
            with st.spinner("Testing connection..."):
                success, message = test_connection()
                if success:
                    st.success(message)
                else:
                    st.error(message)
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        # Display configuration info
        st.markdown("---")
        st.subheader("📋 Configuration")
        st.text(f"Base URL: {st.session_state.client.base_url if st.session_state.client else 'Not connected'}")
        
        # Model information
        if st.session_state.client:
            if st.button("📊 Get Available Models"):
                with st.spinner("Fetching models..."):
                    models_result = st.session_state.client.get_available_models()
                    if models_result["status"] == "success":
                        st.json(models_result["models"])
                    else:
                        st.error(f"Failed to get models: {models_result['message']}")
        
        # Chat info section
        st.markdown("---")
        st.subheader("📊 Chat Info")
        st.metric("Messages", len(st.session_state.messages))
        
        if st.session_state.messages:
            user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
            assistant_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
            
            st.metric("User Messages", user_messages)
            st.metric("Assistant Messages", assistant_messages)
        
        # Export chat
        if st.session_state.messages:
            chat_data = {
                "messages": st.session_state.messages,
                "timestamp": st.session_state.get("chat_start_time", "Unknown")
            }
            
            st.download_button(
                label="📥 Export Chat",
                data=json.dumps(chat_data, indent=2),
                file_name="llama_chat_export.json",
                mime="application/json"
            )
    
    # Main chat interface
    st.subheader("💬 Chat with LLAMA LLM")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input (must be outside any containers)
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Check if we have a connection
        if st.session_state.connection_status != "connected":
            with st.chat_message("assistant"):
                st.error("❌ Not connected to LLAMA LLM. Please test the connection first.")
        else:
            # Display assistant response
            with st.chat_message("assistant"):
                with st.spinner("🤖 LLAMA is thinking..."):
                    response = send_message(prompt)
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main() 