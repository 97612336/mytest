import requests_test

url = 'http://140.143.224.74:8080/v1/get_random_book'

res = requests_test.get(url)
print(res.text)