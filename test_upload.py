import requests
import sys

url = "http://localhost:8000/api/v1/documents/upload"
files = {'file': ('test.txt', 'This is a test document content.')}
data = {'session_id': 'test-session-123'}

try:
    print(f"Testing upload to {url}...")
    response = requests.post(url, files=files, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ SUCCESS: Upload worked locally!")
        sys.exit(0)
    else:
        print("❌ FAILED: Upload failed locally.")
        sys.exit(1)
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)
