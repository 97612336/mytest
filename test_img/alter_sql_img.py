import json
import os

import pymysql
from urllib import request

import requests


# 获取数据库连接对象
def get_db():
    with open("/home/wangkun/conf/sqlconf", "r") as f1:
        res = f1.read()
    sql_dict = json.loads(res)
    config = {
        'host': sql_dict.get("SqlHost"),
        'port': int(sql_dict.get("SqlPort")),
        'user': sql_dict.get("SqlUser"),
        'password': sql_dict.get("SqlPassword"),
        'db': 'novel',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }
    db = pymysql.connect(**config)
    return db


# 获取所有书籍信息
def get_all_book():
    db = get_db()
    sql_str = "select id,book_img from book;"
    cursor = db.cursor()
    cursor.execute(sql_str)
    res = cursor.fetchall()
    cursor.close()
    db.close()
    return res


# 根据url下载图片
def get_img_file_by_url(id, url):
    ext = str(url).split(".")[-1]
    file_name = str(id) + "." + ext
    save_path = "/home/wangkun/static_dir/some_imgs/" + file_name
    res = request.urlretrieve(url, save_path)
    return res[0]


# 上传图片
def upload_one_file(file_path):
    code = os.getenv("code")
    data = {
        "code": code
    }
    try:
        files = {'file': open(file_path, 'rb')}
    except:
        return 0
    url = "https://file.bigbiy.com/skyload"
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36'
    }

    res = requests.post(url, data=data, files=files, headers=headers)
    print("已经上传了,等待响应")
    one_dict = json.loads(res.text)
    if one_dict.get("code") == 200:
        return one_dict.get("url")
    else:
        return 0


# 根据id和url重新设置数据数据
def set_sql_info(id, url):
    db = get_db()
    cursor = db.cursor()
    sql_str = 'update book set book_img="%s" where id=%s;' % (url, id)
    cursor.execute(sql_str)
    db.commit()
    cursor.close()
    db.close()


if __name__ == '__main__':
    # 首先得到所有的书籍信息
    book_list = get_all_book()
    # 遍历书本信息,执行单个操作
    for one_book in book_list:
        id = one_book.get("id")
        img_url = one_book.get("book_img")
        if id > 2057:
            # 根据url下载图片
            try:
                file_path = get_img_file_by_url(id, url=img_url)
                print("已经把图片下载下来了")
                # 把下载下来的图片上传到服务器上
                new_img_url = upload_one_file(file_path)
                print("已经把图片上传到服务器上了")
            except:
                new_img_url = "https://file.bigbiy.com/upload_file/2018-10-18/f9bea1928031f8fe287afb45ec3fc262.png"
            if new_img_url == 0:
                print(file_path)
                new_img_url = "https://file.bigbiy.com/upload_file/2018-10-18/f9bea1928031f8fe287afb45ec3fc262.png"
                print("上传图片错误")
            # 重新设置数据库数据
            set_sql_info(id, new_img_url)
            print("成功更新数据库数据", id)
