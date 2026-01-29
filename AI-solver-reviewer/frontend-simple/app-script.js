// Configuration
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000/api/v1'
    : 'http://13.211.53.117:8000/api/v1';

// State
let sessionId = null;
let selectedFiles = [];
let isUploading = false;
let isSending = false;

// Initialize
document.addEventListener('DOMContentLoaded', init);

function init() {
    // Generate session ID
    sessionId = generateSessionId();
    document.getElementById('session-id').textContent = sessionId;

    // Setup event listeners
    setupUploadArea();
    setupChatInput();
    setupMobileTabs(); // New function

    // Cleanup on page unload
    window.addEventListener('beforeunload', cleanup);
}

function setupMobileTabs() {
    const tabs = document.querySelectorAll('.tab-btn');
    const sidebar = document.getElementById('sidebar-view');
    const chatView = document.getElementById('chat-view');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active'));
            // Add active to clicked
            tab.classList.add('active');

            const target = tab.dataset.tab;
            if (target === 'upload') {
                sidebar.classList.add('active');
                chatView.classList.remove('active');
            } else {
                sidebar.classList.remove('active');
                chatView.classList.add('active');
                // Scroll to bottom of chat
                const messages = document.getElementById('chat-messages');
                messages.scrollTop = messages.scrollHeight;
            }
        });
    });
}

function generateSessionId() {
    return 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
}

function setupUploadArea() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');

    uploadArea.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        selectedFiles = Array.from(e.target.files);
        updateUploadButton();
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        const files = Array.from(e.dataTransfer.files).filter(f =>
            f.name.endsWith('.pdf') || f.name.endsWith('.txt')
        );
        selectedFiles = files;
        fileInput.files = e.dataTransfer.files;
        updateUploadButton();
    });

    uploadBtn.addEventListener('click', uploadFiles);
}

function updateUploadButton() {
    const uploadBtn = document.getElementById('upload-btn');
    const uploadPrompt = document.querySelector('.upload-prompt p');

    if (selectedFiles.length > 0) {
        uploadBtn.style.display = 'block';
        uploadBtn.textContent = `Upload ${selectedFiles.length} file(s)`;
        uploadPrompt.textContent = `${selectedFiles.length} file(s) selected`;
    } else {
        uploadBtn.style.display = 'none';
        uploadPrompt.textContent = 'Click or drag files here';
    }
}

async function uploadFiles() {
    if (isUploading || selectedFiles.length === 0) return;

    isUploading = true;
    const uploadBtn = document.getElementById('upload-btn');
    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Uploading...';

    for (const file of selectedFiles) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('session_id', sessionId);

            const response = await fetch(`${API_BASE_URL}/documents/upload`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }

            const result = await response.json();
            addDocumentToList(file.name, file.size);
            addMessage('assistant', `Successfully uploaded "${file.name}". You can now ask me questions about it!`);

        } catch (error) {
            console.error('Upload error:', error);
            addMessage('error', `Failed to upload "${file.name}": ${error.message}`);
        }
    }

    // Reset
    selectedFiles = [];
    document.getElementById('file-input').value = '';
    updateUploadButton();
    isUploading = false;
    uploadBtn.disabled = false;
}

function addDocumentToList(name, size) {
    const documentList = document.getElementById('document-list');
    const emptyState = documentList.querySelector('.empty-state');
    if (emptyState) emptyState.remove();

    const docItem = document.createElement('div');
    docItem.className = 'document-item';
    docItem.innerHTML = `
        <div class="document-name">${name}</div>
        <div class="document-size">${formatBytes(size)}</div>
    `;
    documentList.appendChild(docItem);
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function setupChatInput() {
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');

    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    chatInput.addEventListener('input', () => {
        chatInput.style.height = 'auto';
        chatInput.style.height = chatInput.scrollHeight + 'px';
    });

    sendBtn.addEventListener('click', sendMessage);
}

async function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();

    if (!message || isSending) return;

    isSending = true;
    const sendBtn = document.getElementById('send-btn');
    sendBtn.disabled = true;

    // Add user message
    addMessage('user', message);
    chatInput.value = '';
    chatInput.style.height = 'auto';

    // Add loading message
    const loadingId = addMessage('loading', 'AI is thinking...');

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                message: message
            })
        });

        if (!response.ok) {
            throw new Error(`Chat failed: ${response.statusText}`);
        }

        const result = await response.json();

        // Remove loading message
        removeMessage(loadingId);

        // Add AI response
        addMessage('assistant', result.response);

    } catch (error) {
        console.error('Chat error:', error);
        removeMessage(loadingId);
        addMessage('error', `Failed to get response: ${error.message}`);
    }

    isSending = false;
    sendBtn.disabled = false;
    chatInput.focus();
}

function addMessage(type, content) {
    const chatMessages = document.getElementById('chat-messages');
    const welcomeMessage = chatMessages.querySelector('.welcome-message');
    if (welcomeMessage) welcomeMessage.remove();

    const messageId = 'msg-' + Date.now();
    const messageEl = document.createElement('div');
    messageEl.id = messageId;
    messageEl.className = `message ${type}`;

    if (type === 'loading') {
        messageEl.innerHTML = `
            <span class="loading-dots">
                <span>.</span><span>.</span><span>.</span>
            </span>
            ${content}
        `;
    } else {
        messageEl.textContent = content;
    }

    chatMessages.appendChild(messageEl);
    messageEl.scrollIntoView({ behavior: 'smooth' });

    return messageId;
}

function removeMessage(messageId) {
    const message = document.getElementById(messageId);
    if (message) message.remove();
}

async function cleanup() {
    if (!sessionId) return;

    try {
        // Send cleanup request (don't wait for response)
        navigator.sendBeacon(`${API_BASE_URL}/session/${sessionId}/cleanup`);
    } catch (error) {
        console.error('Cleanup error:', error);
    }
}
