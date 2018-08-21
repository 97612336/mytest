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


def get_one_file():
    db = get_mysql_db()
    cursor = db.cursor()
    sql = "select chapter_text from chapter where id=1234;"
    cursor.execute(sql)
    res = cursor.fetchone()
    text = res[0]
    with open("c.txt", 'w') as f1:
        f1.write(text)
    cursor.close()
    db.close()


if __name__ == '__main__':
    get_one_file()
