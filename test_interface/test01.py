import requests

url = 'http://140.143.224.74:8080/v1/get_random_book'

res = requests.get(url)
print(res.text)