import requests
import json
import os
from dotenv import load_dotenv

url = "https://api.openai.com/v1/chat/completions"

openai_api_key = os.getenv("openai_api_key")

headers = {
    "Content Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}
data = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role":"user","content":"Quanto é 1+1?"}]
}

response = requests.post(url, headers = headers, data = json.dumps(data))

print(response.json()['choices'][0]['message']['content'])