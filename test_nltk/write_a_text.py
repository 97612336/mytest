import json
import os

# 获取MySQL的配置文件
import pymysql


def get_mysql_conf():
    user_home = os.environ.get("HOME")
    conf_base_path = user_home + "/conf"
    mysql_conf_path = conf_base_path + "/mysql.conf"
    with open(mysql_conf_path, "r") as f1:
        res_str = f1.read()
    mysql_dict = json.loads(res_str)
    return mysql_dict


# 链接数据库,返回db对象
def get_mysql_db():
    # 获取配置文件
    mysql_dict = get_mysql_conf()
    # 链接数据库
    connection = pymysql.connect(host=mysql_dict.get("host"), user=mysql_dict.get("user"),
                                 password=mysql_dict.get("password"), port=mysql_dict.get("port"),
                                 db=mysql_dict.get("db"), charset='utf8')
    return connection


def get_text():
    db = get_mysql_db()
    cursor = db.cursor()

    chapter_list = []
    sql = 'select chapter_text from chapter where book_id=47 ;'

    cursor.execute(sql)

    res = cursor.fetchall()

    for one in res:
        chapter_list.append(one[0])
    cursor.close()
    db.close()
    return chapter_list


def get_all_book_list(chapter_list):
    book_list = []
    chapter_list = get_text()
    for one in chapter_list:
        one_chapter_list = json.loads(one)
        for one_paragraph in one_chapter_list:
            book_list.append(one_paragraph)
    return book_list


def write_book(book_list):
    for one in book_list:
        with open('./a.txt', 'a+') as f1:
            f1.write(one)
            print("写入一段")
    print("写入完成")


def main():
    chapter_list = get_text()
    book_list = get_all_book_list(chapter_list)
    write_book(book_list)


# main()
