import requests
import time

with open("a.png", "rb") as f1:
    data = f1.read()
url = "http://image.baidu.com/pcdutu/a_upload?fr=html5&target=pcSearchImage&needJson=true"

files = {'file': open('a.png', 'rb')}
res = requests.post(url,files=files)
print(res.text)