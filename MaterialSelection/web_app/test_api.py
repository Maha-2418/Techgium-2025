import requests
import json
import threading
import time
from server import app

def run_server():
    app.run(port=5001)

def test_api():
    # Start server in thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(2) # Wait for startup
    
    url = "http://127.0.0.1:5001/api/query"
    payload = {"query": "Need high tensile strength"}
    
    print(f"Testing API at {url} with: {payload}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
        
        resp_data = response.json()
        if response.status_code == 200 and resp_data.get("type") == "recommendation":
             print("\n✅ API Verification PASSED")
        else:
             print(f"\n❌ API Verification FAILED. Type: {resp_data.get('type')}")
             
    except Exception as e:
        print(f"\n❌ API Verification FAILED with error: {e}")

if __name__ == "__main__":
    test_api()
