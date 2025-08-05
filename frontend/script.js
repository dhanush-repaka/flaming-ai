// Global variables
let isConnected = false;
let conversationHistory = [];
let messageCount = 0;
let userMessageCount = 0;
let assistantMessageCount = 0;

// DOM elements
const elements = {
    connectionStatus: document.getElementById('connectionStatus'),
    statusIndicator: document.getElementById('statusIndicator'),
    statusText: document.getElementById('statusText'),
    connectionSection: document.getElementById('connectionSection'),
    chatSection: document.getElementById('chatSection'),
    testConnectionBtn: document.getElementById('testConnectionBtn'),
    testResults: document.getElementById('testResults'),
    messageInput: document.getElementById('messageInput'),
    sendMessageBtn: document.getElementById('sendMessageBtn'),
    chatMessages: document.getElementById('chatMessages'),
    charCount: document.getElementById('charCount'),
    typingIndicator: document.getElementById('typingIndicator'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    loadingText: document.getElementById('loadingText'),
    clearChatBtn: document.getElementById('clearChatBtn'),
    exportChatBtn: document.getElementById('exportChatBtn'),
    getModelsBtn: document.getElementById('getModelsBtn'),
    modelsModal: document.getElementById('modelsModal'),
    modelsContent: document.getElementById('modelsContent'),
    closeModelsModal: document.getElementById('closeModelsModal'),
    sidebarStatus: document.getElementById('sidebarStatus'),
    sidebarUrl: document.getElementById('sidebarUrl'),
    totalMessages: document.getElementById('totalMessages'),
    userMessages: document.getElementById('userMessages'),
    assistantMessages: document.getElementById('assistantMessages'),
    welcomeTime: document.getElementById('welcomeTime')
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    setWelcomeTime();
});

function initializeApp() {
    // Set initial state
    updateConnectionStatus('not_connected');
    updateMessageCounts();
}

function setupEventListeners() {
    // Connection test button
    elements.testConnectionBtn.addEventListener('click', testConnection);
    
    // Message input
    elements.messageInput.addEventListener('input', handleMessageInput);
    elements.messageInput.addEventListener('keydown', handleKeyDown);
    
    // Send message button
    elements.sendMessageBtn.addEventListener('click', sendMessage);
    
    // Chat controls
    elements.clearChatBtn.addEventListener('click', clearChat);
    elements.exportChatBtn.addEventListener('click', exportChat);
    
    // Models button
    elements.getModelsBtn.addEventListener('click', getAvailableModels);
    elements.closeModelsModal.addEventListener('click', closeModelsModal);
    
    // Modal backdrop
    elements.modelsModal.addEventListener('click', function(e) {
        if (e.target === elements.modelsModal) {
            closeModelsModal();
        }
    });
}

function setWelcomeTime() {
    const now = new Date();
    elements.welcomeTime.textContent = now.toLocaleTimeString();
}

// Connection Testing
async function testConnection() {
    showLoading('Testing connection...');
    
    try {
        const response = await fetch('/api/test-connection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            showTestResults(true, result);
            updateConnectionStatus('connected');
            showChatInterface();
        } else {
            showTestResults(false, result);
            updateConnectionStatus('failed');
        }
    } catch (error) {
        console.error('Connection test failed:', error);
        showTestResults(false, {
            message: 'Network error: Unable to connect to the server',
            details: error.message
        });
        updateConnectionStatus('failed');
    } finally {
        hideLoading();
    }
}

function showTestResults(success, result) {
    elements.testResults.style.display = 'block';
    elements.testResults.className = `test-results ${success ? 'success' : 'error'}`;
    
    const icon = success ? '✅' : '❌';
    const title = success ? 'Connection Successful!' : 'Connection Failed';
    
    elements.testResults.innerHTML = `
        <h4>${icon} ${title}</h4>
        <p>${result.message}</p>
        ${result.details ? `<ul><li>${result.details}</li></ul>` : ''}
        ${success ? '<p>You can now start chatting with LLAMA LLM!</p>' : ''}
    `;
}

function updateConnectionStatus(status) {
    const statusConfig = {
        'not_connected': { text: 'Not Connected', indicator: '' },
        'connected': { text: 'Connected', indicator: 'connected' },
        'failed': { text: 'Connection Failed', indicator: 'failed' }
    };
    
    const config = statusConfig[status];
    elements.statusText.textContent = config.text;
    elements.statusIndicator.className = `status-indicator ${config.indicator}`;
    elements.sidebarStatus.textContent = config.text;
    
    isConnected = status === 'connected';
    elements.sendMessageBtn.disabled = !isConnected;
}

function showChatInterface() {
    elements.connectionSection.style.display = 'none';
    elements.chatSection.style.display = 'grid';
    elements.sidebarUrl.textContent = 'https://prdus-gateway-llm-large.app-prd-eus-204.k8s.munichre.com';
}

// Message Handling
function handleMessageInput() {
    const text = elements.messageInput.value;
    const charCount = text.length;
    
    elements.charCount.textContent = `${charCount}/2000`;
    elements.sendMessageBtn.disabled = !isConnected || charCount === 0;
    
    // Auto-resize textarea
    elements.messageInput.style.height = 'auto';
    elements.messageInput.style.height = Math.min(elements.messageInput.scrollHeight, 120) + 'px';
}

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        if (!elements.sendMessageBtn.disabled) {
            sendMessage();
        }
    }
}

async function sendMessage() {
    const message = elements.messageInput.value.trim();
    if (!message || !isConnected) return;
    
    // Add user message to chat
    addMessageToChat('user', message);
    elements.messageInput.value = '';
    handleMessageInput();
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                conversation_history: conversationHistory
            })
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            addMessageToChat('assistant', result.message);
        } else {
            addMessageToChat('assistant', `Error: ${result.message}`, true);
        }
    } catch (error) {
        console.error('Chat error:', error);
        addMessageToChat('assistant', 'Error: Unable to send message', true);
    } finally {
        hideTypingIndicator();
    }
}

function addMessageToChat(role, content, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = content;
    if (isError) {
        messageText.style.color = '#f44336';
    }
    
    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = new Date().toLocaleTimeString();
    
    messageContent.appendChild(messageText);
    messageContent.appendChild(messageTime);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    
    // Remove welcome message if it exists
    const welcomeMessage = elements.chatMessages.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    elements.chatMessages.appendChild(messageDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
    
    // Update conversation history
    conversationHistory.push({
        role: role,
        content: content
    });
    
    // Update message counts
    if (role === 'user') {
        userMessageCount++;
    } else {
        assistantMessageCount++;
    }
    messageCount++;
    updateMessageCounts();
}

function showTypingIndicator() {
    elements.typingIndicator.style.display = 'flex';
}

function hideTypingIndicator() {
    elements.typingIndicator.style.display = 'none';
}

function updateMessageCounts() {
    elements.totalMessages.textContent = messageCount;
    elements.userMessages.textContent = userMessageCount;
    elements.assistantMessages.textContent = assistantMessageCount;
}

// Chat Controls
function clearChat() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        elements.chatMessages.innerHTML = `
            <div class="welcome-message">
                <div class="message assistant">
                    <div class="message-avatar">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="message-content">
                        <div class="message-text">
                            Hello! I'm LLAMA LLM. How can I help you today?
                        </div>
                        <div class="message-time">${new Date().toLocaleTimeString()}</div>
                    </div>
                </div>
            </div>
        `;
        
        conversationHistory = [];
        messageCount = 0;
        userMessageCount = 0;
        assistantMessageCount = 0;
        updateMessageCounts();
    }
}

function exportChat() {
    const chatData = {
        messages: conversationHistory,
        timestamp: new Date().toISOString(),
        statistics: {
            total: messageCount,
            user: userMessageCount,
            assistant: assistantMessageCount
        }
    };
    
    const dataStr = JSON.stringify(chatData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `llama_chat_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
    link.click();
}

// Models
async function getAvailableModels() {
    showLoading('Fetching available models...');
    
    try {
        const response = await fetch('/api/models', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            showModelsModal(result.models);
        } else {
            alert(`Failed to get models: ${result.message}`);
        }
    } catch (error) {
        console.error('Models error:', error);
        alert('Error: Unable to fetch models');
    } finally {
        hideLoading();
    }
}

function showModelsModal(models) {
    let content = '';
    
    if (models.data && models.data.length > 0) {
        content = '<div class="models-list">';
        models.data.forEach(model => {
            content += `
                <div class="model-item">
                    <h4>${model.id || 'Unknown Model'}</h4>
                    ${model.object ? `<p><strong>Type:</strong> ${model.object}</p>` : ''}
                    ${model.created ? `<p><strong>Created:</strong> ${new Date(model.created * 1000).toLocaleDateString()}</p>` : ''}
                </div>
            `;
        });
        content += '</div>';
    } else {
        content = '<p>No models found or different response format.</p>';
    }
    
    elements.modelsContent.innerHTML = content;
    elements.modelsModal.style.display = 'flex';
}

function closeModelsModal() {
    elements.modelsModal.style.display = 'none';
}

// Loading
function showLoading(text) {
    elements.loadingText.textContent = text;
    elements.loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    elements.loadingOverlay.style.display = 'none';
}

// Utility functions
function formatTime(date) {
    return date.toLocaleTimeString();
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
});

// Add some CSS for models modal
const style = document.createElement('style');
style.textContent = `
    .models-list {
        max-height: 400px;
        overflow-y: auto;
    }
    
    .model-item {
        padding: 15px;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        margin-bottom: 10px;
        background: #f9f9f9;
    }
    
    .model-item h4 {
        margin: 0 0 10px 0;
        color: #333;
    }
    
    .model-item p {
        margin: 5px 0;
        color: #666;
        font-size: 0.9rem;
    }
`;
document.head.appendChild(style); 