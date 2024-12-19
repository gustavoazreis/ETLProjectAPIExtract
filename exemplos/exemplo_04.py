import requests
import json

url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content Type": "application/json",
    "Authorization": "Bearer xxx"
}
data = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role":"user","content":"Quanto é 1+1?"}]
}

response = requests.post(url, headers = headers, data = json.dumps(data))

print(response.json()['choices'][0]['message']['content'])