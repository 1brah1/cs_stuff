import requests
import sys

url = "http://localhost:8000/api/v1/chat"
headers = {"Content-Type": "application/json"}
data = {
    "session_id": "test-session-chat-1",
    "message": "Hello, can you help me?"
}

try:
    print(f"Testing chat to {url}...")
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ SUCCESS: Chat endpoint reachable!")
        if "Please upload at least one document" in response.text:
             print("   (Correctly validated no documents)")
        sys.exit(0)
    else:
        print(f"❌ FAILED: Chat failed with {response.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)
