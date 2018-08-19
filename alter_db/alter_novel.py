import json
import os

import pymysql


def get_mysql_db():
    home_path = os.getenv("HOME")
    conf_file_path = home_path + "/conf/sqlconf"
    with open(conf_file_path, "r") as f:
        conf_str = f.read()
    conf_dict = json.loads(conf_str)
    conn = pymysql.connect(host=conf_dict.get("SqlHost"), port=int(conf_dict.get("SqlPort")),
                           user=conf_dict.get("SqlUser"), password=conf_dict.get("SqlPassword"),
                           db="novel", charset='utf8mb4')
    return conn


def get_all_book__id_list():
    conn = get_mysql_db()
    cursor = conn.cursor()
    sql = "select id from book where has_chapter=1;"
    cursor.execute(sql)
    res = cursor.fetchall()
    id_list = []
    for one in res:
        one_id = one[0]
        id_list.append(one_id)
    cursor.close()
    conn.close()
    return id_list


def update_book_by_id(one_id):
    conn = get_mysql_db()
    cursor = conn.cursor()
    sql = "select chapter_text from chapter where book_id=%s limit 1;" % one_id
    cursor.execute(sql)
    res = cursor.fetchone()
    one_chapter_list_text = res[0]
    try:
        tmp_res = json.loads(one_chapter_list_text)
    except:
        print("出错一次")
        update_sql = "update book set has_chapter=0 where id=%s;" % one_id
        cursor.execute(update_sql)
        conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    id_list = get_all_book__id_list()
    for one in id_list:
        update_book_by_id(one)
