import time
import redis
import datetime
import json
import os
from lxml import etree

import chardet
import pymysql
import requests_test

baidu_url = "http://www.baidu.com/baidu?wd="
baidu_fengyun_url = "http://top.baidu.com/"


def get_mysql_db():
    home_path = os.getenv("HOME")
    conf_file_path = home_path + "/conf/sqlconf"
    with open(conf_file_path, "r") as f:
        conf_str = f.read()
    conf_dict = json.loads(conf_str)
    conn = pymysql.connect(host=conf_dict.get("SqlHost"), port=int(conf_dict.get("SqlPort")),
                           user=conf_dict.get("SqlUser"), password=conf_dict.get("SqlPassword"),
                           db="bigbiy_web", charset='utf8mb4')
    return conn


# 获取URL的网页HTML
def get_html_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    }
    try:
        res = requests_test.get(url, headers=headers)
    except:
        print("一条记录不能解析%s" % (datetime.datetime.now()))
        return ""
    html_bytes = res.content
    code_style = chardet.detect(html_bytes).get("encoding")
    try:
        html_text = html_bytes.decode(code_style, "ignore")
    except:
        print(datetime.datetime.now())
        print("encoding is error")
        return ''
    return html_text


def html_parser(html_text, compl_str):
    # 解析HTML文件
    try:
        tree = etree.HTML(html_text)
        res = tree.xpath(compl_str)
    except:
        print(datetime.datetime.now())
        print("can't parse html")
        return
    return res


# 得到热搜的关键词
def get_fengyun_words():
    fengyun_res = get_html_text(baidu_fengyun_url)
    words_list = html_parser(fengyun_res,
                             '//*[@id="box-cont"]/div[3]/div[2]/div/div[2]/div[1]/ul/li/div[1]/a[1]/text()')
    res_str = ""
    for one_word in words_list:
        if res_str:
            res_str = res_str + "," + one_word
        else:
            res_str = one_word
    return res_str


def save_to_redis(hot_words):
    r = redis.StrictRedis()
    r.set("hot_words", hot_words, ex=86400)


if __name__ == '__main__':
    while 1:
        hot_words = get_fengyun_words()
        save_to_redis(hot_words)
        print("success,", datetime.datetime.now())
        time.sleep(86000)
