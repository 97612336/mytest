import json

import requests_test


def upload_img(img_path):
    # url = "http://image.baidu.com/pcdutu/a_upload?fr=html5&target=pcSearchImage&needJson=true"
    url = "https://sm.ms/api/upload"

    # files = {'file': open(img_path, 'rb')}
    files = {"smfile": open(img_path, 'rb')}
    res = requests_test.post(url, files=files)
    json_res = json.loads(res.text)
    return json_res

# res = upload_img('a.png')
# print(res)
