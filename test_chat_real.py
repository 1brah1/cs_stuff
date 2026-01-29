import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"
SESSION_ID = "test-session-real-1"

# 1. Upload
print(f"Uploading document to session {SESSION_ID}...")
files = {'file': ('test_real.txt', 'This is a real test document content about safety.')}
data = {'session_id': SESSION_ID}
try:
    resp = requests.post(f"{BASE_URL}/documents/upload", files=files, data=data) 
    # Note: data={'session_id':...} sends as form fields, which my documents.py 'session_id: str = Form(...)' expects.
    print(f"Upload Status: {resp.status_code}")
    print(f"Upload Response: {resp.text}")
    if resp.status_code != 200:
        print("❌ Upload failed")
        sys.exit(1)
except Exception as e:
    print(f"❌ Upload Error: {e}")
    sys.exit(1)

# 2. Chat
print("Testing chat...")
chat_data = {
    "session_id": SESSION_ID,
    "message": "What is this document about?"
}
try:
    resp = requests.post(f"{BASE_URL}/chat", json=chat_data)
    print(f"Chat Status: {resp.status_code}")
    print(f"Chat Response: {resp.text}")
    
    if resp.status_code == 200:
        print("✅ SUCCESS: Chat worked!")
    else:
        print("❌ FAILED: Chat returned error")
        sys.exit(1)

except Exception as e:
    print(f"❌ Chat Error: {e}")
    sys.exit(1)
