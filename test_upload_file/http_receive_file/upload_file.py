import os
import hashlib
import datetime

import requests


# url = "https://file.bigbiy.com/skyload"

# 执行读取文件上传的操作
def uplaod_file(file_path, url):
    # 获取总共需要上传多少次
    size_bytes = os.path.getsize(file_path)
    one_size_byte = 1024 * 1024
    upload_times = int(size_bytes / one_size_byte)
    # 获取文件的信息和后缀
    tmp_path_name, file_name = os.path.split(file_path)
    short_name, ext_name = os.path.splitext(file_name)
    # 根据文件名获取md5的字符串
    md5_file_name = get_md5_str(file_name)
    # 一次读取文件的5M二进制信息，发送给服务器
    n = 1
    uploaded_url = ""
    with open(file_path, "rb") as f:
        while 1:
            data = f.read(one_size_byte)
            res_text = upload_one_file(data, md5_file_name, ext_name, url)
            uploaded_url = res_text
            if upload_times != 0:
                upload_percent = float(n / upload_times) * 100
            else:
                upload_percent = 100
            print("%d%%" % upload_percent)
            n = n + 1
            if len(data) == 0:
                break
    return uploaded_url


# 单个分片文件上传的操作
def upload_one_file(file, file_name, ext, url):
    code = "wangkun_123"
    data = {
        "code": code,
        "ext": ext,
        "file_name": file_name
    }
    files = {'file': file}
    res = requests.post(url, data=data, files=files)
    return res.text


# 生成MD5的方法
def get_md5_str(one_str):
    m = hashlib.md5()
    new_str = one_str + str(datetime.datetime.now())
    m.update(new_str.encode("utf-8"))
    return m.hexdigest()


if __name__ == '__main__':
    file_path = "style.css"
    # url = "http://127.0.0.1:8011"
    url = "https://file.bigbiy.com/upload"
    file_url = uplaod_file(file_path, url)
    print(file_url)
