import json
import os

import pymysql
import psycopg2


# 获取mysql的链接
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


# 获取postgresql的连接
def get_postgresql_db():
    home_path = os.getenv("HOME")
    config_file_path = home_path + "/conf/postgresql_conf"
    with open(config_file_path) as f:
        conf_str = f.read()
    conf_dict = json.loads(conf_str)
    conn = psycopg2.connect(host=conf_dict.get("host"), port=conf_dict.get("port"),
                            user=conf_dict.get("user"), password=conf_dict.get("password"),
                            database="mydb")
    return conn


# 读取分页数
def read_mysql_data(page_num, page_size):
    conn = get_mysql_db()
    cursor = conn.cursor()
    sql = "select * from book limit %s,%s;" % (page_size * (page_num - 1), page_size)
    cursor.execute(sql)
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res


# 根据mysql查询得到的结果列表,插入新数据到postgresql
def write_data_to_postgresql(res):
    db = get_postgresql_db()
    cursor = db.cursor()
    for one in res:
        id = one[0]
        name = one[1]
        create_time = one[2]
        url = one[3]
        book_img = one[4]
        kind = one[5]
        author = one[6]
        has_chapter = one[7]
        sql = "insert into book values (%s,'%s','%s','%s','%s','%s','%s',%s)" % (
            id, name, create_time, url, book_img, kind, author, has_chapter
        )
        cursor.execute(sql)
        db.commit()
    cursor.close()
    db.close()

# 主方法
if __name__ == '__main__':
    page_size = 100
    n = 1
    while 1:
        res = read_mysql_data(n, page_size)
        if len(res) < 1:
            break
        write_data_to_postgresql(res)
        print(n)
        n = n + 1
