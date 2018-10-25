import requests_test

res = requests_test.get("https://localhost/a.txt")
print(res.text)