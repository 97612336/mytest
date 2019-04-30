# 获取配置文件列表
import pickle

from parse_spider_things import util


def get_info_list():
    with open('urls_list.pickle', "rb") as f:
        res_list = pickle.load(f)
    return res_list


# 根据一个视频页面url获取视频的资源地址
def get_video_source(url):
    html_text = util.get_html_text(url)
    # 获取影片的观看次数，小于5000直接返回0
    num_compl = '//*[@id="main_video_block"]/div[12]/span[2]/text()'
    nums = util.html_parser(html_text, num_compl)
    try:
        look_num = int(nums[0])
    except:
        return 0
    if look_num > 10000:
        # 获取视频资源地址
        res = util.html_parser(html_text, '//source/@src')
        movie_href = 0
        if len(res) > 1:
            movie_href = res[1]
        return movie_href
    else:
        return 0


res_list = get_info_list()
res_list.pop()
res_list.pop(0)
for one_kind in res_list:
    print(one_kind.get('kind_name'))
    kind_content = one_kind.get('kind_content')
    for i in kind_content:
        name = i.get('name')
        img = i.get('img')
        url = i.get('url')
        video_url = get_video_source(url)
        if video_url:
            print(name)
            print(img)
            print(video_url)
    print('====================')
