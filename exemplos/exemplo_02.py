import requests

url = 'https://jsonplaceholder.typicode.com/comments'
params = {"postId":1} # Obter apenas comentários do postId = 1
response = requests.get(url, params = params)

comments = response.json()

print(f'Foram encontrados {len(comments)} comentários.')
print(f'Erro: {response.status_code} - {response.text}')