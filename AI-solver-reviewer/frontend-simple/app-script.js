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
    setupChatInput();
    setupAttachment();

    // Cleanup on page unload
    window.addEventListener('beforeunload', cleanup);
}

function generateSessionId() {
    return 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
}

function setupAttachment() {
    const attachBtn = document.getElementById('attach-btn');
    const fileInput = document.getElementById('file-input');
    
    attachBtn.addEventListener('click', () => {
        if (!isUploading) {
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', (e) => {
        const files = Array.from(e.target.files).filter(f =>
            f.name.endsWith('.pdf') || f.name.endsWith('.txt')
        );
        if(files.length > 0) {
            selectedFiles = files;
            displayFilePills();
            uploadFiles();
        }
    });
}

function displayFilePills() {
    const container = document.getElementById('file-pills-container');
    container.innerHTML = ''; // clear existing
    selectedFiles.forEach(file => {
        const pill = document.createElement('div');
        pill.className = 'file-pill';
        pill.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
            <span class="file-name">${file.name}</span>
            <span class="upload-status">Uploading...</span>
        `;
        container.appendChild(pill);
    });
}

function clearFilePills() {
    const container = document.getElementById('file-pills-container');
    container.innerHTML = '';
    selectedFiles = [];
}

async function uploadFiles() {
    if (isUploading || selectedFiles.length === 0) return;

    isUploading = true;
    const attachBtn = document.getElementById('attach-btn');
    attachBtn.disabled = true;

    // Clear Welcome Hero
    const hero = document.getElementById('welcome-hero');
    if(hero) hero.style.display = 'none';

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

            // Update pill UI
            const pills = document.querySelectorAll('.file-pill');
            pills.forEach(pill => {
                if(pill.textContent.includes(file.name)) {
                    pill.classList.add('success');
                    pill.querySelector('.upload-status').textContent = 'Ready';
                }
            });

            addMessage('system', `Successfully uploaded "${file.name}". I can now analyze it for you.`);

        } catch (error) {
            console.error('Upload error:', error);
            addMessage('error', `Failed to upload "${file.name}": ${error.message}`);
        }
    }

    document.getElementById('file-input').value = '';
    isUploading = false;
    attachBtn.disabled = false;
    
    // Clear the pills automatically after 5 seconds
    setTimeout(clearFilePills, 5000);
}

function setupChatInput() {
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');

    chatInput.addEventListener('keydown', (e) => {
        // Prevent default enter behavior and send message if shift isn't pressed
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    chatInput.addEventListener('input', () => {
        // Auto resize height
        chatInput.style.height = 'auto';
        chatInput.style.height = Math.min(chatInput.scrollHeight, 200) + 'px';
        
        // Toggle send button state
        if(chatInput.value.trim() !== '') {
            sendBtn.disabled = false;
            sendBtn.classList.add('active');
        } else {
            sendBtn.disabled = true;
            sendBtn.classList.remove('active');
        }
    });

    sendBtn.addEventListener('click', sendMessage);
}

async function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();

    if (!message || isSending) return;

    // Reset input states
    isSending = true;
    const sendBtn = document.getElementById('send-btn');
    sendBtn.disabled = true;
    sendBtn.classList.remove('active');
    
    // Create User DOM Node
    addMessage('user', message);
    chatInput.value = '';
    chatInput.style.height = 'auto';

    // Clear Welcome Hero
    const hero = document.getElementById('welcome-hero');
    if(hero) hero.style.display = 'none';

    // Spawn loading state
    const loadingId = addMessage('loading', '');

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
        removeMessage(loadingId);
        addMessage('assistant', result.response);

    } catch (error) {
        console.error('Chat error:', error);
        removeMessage(loadingId);
        addMessage('error', `Failed to get response: ${error.message}`);
    }

    isSending = false;
    chatInput.focus();
}

// Generate the message blocks dynamically
function addMessage(type, content) {
    const chatMessages = document.getElementById('chat-messages');

    const messageId = 'msg-' + Date.now();
    const messageWrapper = document.createElement('div');
    messageWrapper.id = messageId;
    messageWrapper.className = `message-wrapper ${type}-wrapper`;
    
    const messageEl = document.createElement('div');
    messageEl.className = `message ${type}`;

    if (type === 'loading') {
        const loader = document.createElement('div');
        loader.className = 'spinner';
        messageEl.appendChild(loader);
    } else if (type === 'assistant') {
        // We use marked parse because previously we injected marked.min.js into the html
        messageEl.innerHTML = marked.parse(content);
    } else {
        messageEl.textContent = content; // For pure text payloads like user/system overrides
    }

    messageWrapper.appendChild(messageEl);
    chatMessages.appendChild(messageWrapper);
    
    // Smooth auto scroll to the new message
    chatMessages.parentNode.scrollTo({
        top: chatMessages.parentNode.scrollHeight,
        behavior: 'smooth'
    });

    return messageId;
}

function removeMessage(messageId) {
    const wrapper = document.getElementById(messageId);
    if (wrapper) wrapper.remove();
}

async function cleanup() {
    if (!sessionId) return;
    try {
        navigator.sendBeacon(`${API_BASE_URL}/session/${sessionId}/cleanup`);
    } catch (error) {
        console.error('Cleanup error:', error);
    }
}
