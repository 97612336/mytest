import json
import os

import requests_test


def uplaod_one_file(file_path):
    code = os.getenv("code")
    data = {
        "code": code
    }

    files = {'file': open(file_path, 'rb')}
    url = "https://file.bigbiy.com/skyload"
    res = requests_test.post(url, data=data, files=files)
    one_dict = json.loads(res.text)
    if one_dict.get("code") == 200:
        return one_dict.get("url")


if __name__ == '__main__':
    url = uplaod_one_file("a.txt")
    print(url)
