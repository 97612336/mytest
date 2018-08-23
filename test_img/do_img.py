import os

from test_img.search_tsz_photos import Search_tsz_photos
import urllib.request as ur

from test_qiniu.test_upload_img_to_sm import upload_img
from utils.get_md5 import get_md5_str


def wirte_url_to_local(url):
    response = ur.urlopen(url)
    data = response.read()
    file_name = get_md5_str(url)
    ext = ".jpg"
    with open("./imgs/" + file_name + ext, "wb") as f:
        f.write(data)
    file_path = "imgs/" + file_name + ext
    res = upload_img(file_path)
    os.remove(file_path)
    return res.get("data").get("url")


if __name__ == '__main__':
    stp = Search_tsz_photos()
    res_list = stp.get_all_photo("汽车")
    # qhimg
    i = 1
    for one in res_list:
        img_url = wirte_url_to_local(one.get("larger_photo"))
        with open('a.txt', 'a+') as f:
            f.write(img_url + "\n")
        print(i)
        i = i + 1
