import requests

url = "http://127.0.0.1:5001/chatbot"  # replace with your exact route if different

payload = {
    "message": "Hello, this is a test"
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response:", response.text)
