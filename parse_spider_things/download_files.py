import os
import pickle
import gevent
import requests

from spider_something import util


# 获取配置文件列表
def get_info_list():
    with open('urls_list.pickle', "rb") as f:
        res_list = pickle.load(f)
    return res_list


# 创建文件夹，并返回路径
def make_dirs(root_dirs, new_dir_name):
    dir_path = root_dir + str(new_dir_name).strip() + "\\"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


# 根据一个视频页面url获取视频的资源地址
def get_video_source(url):
    html_text = util.get_html_text(url)
    # 获取影片的观看次数，小于5000直接返回0
    num_compl = '//*[@id="main_video_block"]/div[12]/span[2]/text()'
    nums = util.html_parser(html_text, num_compl)
    print(nums)
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
            print(url)
        return movie_href
    else:
        return 0


# 根据影片链接下载到本地
def download_by_href(file_path, url):
    movie_bytes = requests.get(url, stream=True)
    with open(file_path, 'wb') as f:
        for chunk in movie_bytes.iter_content(chunk_size=512 * 3):
            if chunk:
                f.write(chunk)


# 根据kind_dir和文件名，执行下载
def download_to_dir(kind_dir_path, movie_title, img_href, gif_href, movie_href):
    # 首先拼接路径
    movie_dir_path = kind_dir_path + movie_title + "\\"
    print(movie_dir_path)
    # 检查该路径是否存在，如果存在，则不继续运行
    if os.path.exists(movie_dir_path):
        return
    # 否则就创建文件夹
    os.makedirs(movie_dir_path)
    # 然后拼接图片
    img_path = movie_dir_path + movie_title + ".jpg"
    download_by_href(img_path, img_href)
    # 然后拼接gif
    gif_path = movie_dir_path + "gif" + movie_title + ".mp4"
    download_by_href(gif_path, gif_href)
    # 拼接视频path
    movie_path = movie_dir_path + movie_title + ".mp4"
    download_by_href(movie_path, movie_href)


if __name__ == '__main__':
    root_dir = "H:\英雄时刻\\48677486\something\\"
    info_list = get_info_list()
    # 获取每个类别下的内容
    i = 0
    for one in info_list:
        kind_name = one.get("kind_name")
        kind_dir_path = make_dirs(root_dir, kind_name)
        # 分析类别下的内容
        kind_content = one.get("kind_content")
        # 创建协程数组
        for one_content in kind_content:
            # 解析具体的视频页面
            video_url = one_content.get("url")
            movie_href = get_video_source(video_url)
            gevent.spawn()
            if movie_href:
                movie_title = one_content.get("name")
                img_href = one_content.get("img")
                gif_href = one_content.get("gif")
                print(kind_dir_path, movie_title, img_href, gif_href, movie_href)
                # 创建协程对象方法，把创建的协程方法加入到gevent_list中去
                download_to_dir(kind_dir_path, movie_title, img_href, gif_href, movie_href)
                i = i + 1
            print(i)
