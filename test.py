import requests

url = "http://127.0.0.1:8000/items/10?q=fastapi"
response = requests.get(url)
print(response.json())
