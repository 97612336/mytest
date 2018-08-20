import requests

res = requests.get("https://localhost/a.txt")
print(res.text)