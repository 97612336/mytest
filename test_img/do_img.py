from test_img.search_tsz_photos import Search_tsz_photos
import urllib.request as ur

from utils.get_md5 import get_md5_str


def wirte_url_to_local(url):
    response = ur.urlopen(url)
    data = response.read()
    file_name = get_md5_str(url)
    ext = ".jpg"
    with open("./imgs/" + file_name + ext, "wb") as f:
        f.write(data)
    return "imgs/" + file_name + ext


if __name__ == '__main__':
    stp = Search_tsz_photos()
    res_list = stp.get_all_photo("汽车")
    # qhimg
    for one in res_list[:2]:
        wirte_url_to_local(one.get("larger_photo"))
        # print(one)
