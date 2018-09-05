import configparser
import json
import os

import pymysql
import time
from elasticsearch_dsl import Document, Text, Integer
from elasticsearch_dsl.connections import connections


def get_db_connection():
    home = os.environ['HOME']
    inifile = '{}/.afsaas.cnf'.format(home)
    config = configparser.ConfigParser()
    config.read(inifile)
    user = config.get('client', 'user')
    password = config.get('client', 'password')
    host = config.get('client', 'host')
    config = {
        'host': host,
        'port': 3306,
        'user': user,
        'password': password,
        'db': 'cyx',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }
    connection = pymysql.connect(**config)
    return connection


# 获取文章的方法
def get_article(n):
    page_size = 20
    db = get_db_connection()
    cursor = db.cursor()
    sql_str = 'select * from art_recommends limit %s,%s;' % ((n - 1) * page_size, page_size)

    cursor.execute(sql_str)
    res = cursor.fetchall()
    res_list = []
    for one_article in res:
        tmp = {}
        tmp['id'] = one_article.get('id')
        tmp['title'] = one_article.get('title')
        tmp['car_name'] = one_article.get('car_name')
        tmp['author'] = one_article.get("author")
        comment_str = one_article.get('comment')
        try:
            # 当解析json字符串不合规的时候,跳过本次循环
            comment_list = json.loads(comment_str)
        except:
            continue
        comment = ''
        for one_comment in comment_list:
            if 'comment' in one_comment.keys():
                comment = comment + '  ' + one_comment.get('comment')
        tmp['comment'] = comment
        res_list.append(tmp)
    cursor.close()
    db.close()
    return res_list


# 定义一个文档类
class Articles(Document):
    title = Text(analyzer='ik_max_word')
    id = Integer()
    author = Text(analyzer='ik_max_word')
    comment = Text(analyzer='ik_max_word')
    car_name = Text(analyzer='ik_max_word')

    class Index:
        name = 'cyx'


# 执行保存到elasticsearch的方法
def save_to_es(res_list):
    Articles.init()
    for one in res_list:
        aid = one.get('id')
        title = one.get('title')
        author = one.get('author')
        comment = one.get('comment')
        car_name = one.get('car_name')
        es_article = Articles(meta={'id': aid})
        es_article.title = title
        es_article.author = author
        es_article.comment = comment
        es_article.car_name = car_name
        es_article.id = aid
        es_article.save()
        print('成功保存了一条数据%s' % aid)


if __name__ == '__main__':
    start_time = time.time()
    connections.create_connection(hosts=['127.0.0.1:1235'])
    i = 1
    while True:
        articles = get_article(i)
        if len(articles) == 0:
            break
        save_to_es(articles)
        i = i + 1
    end_time = time.time()
    print('共花费了%s秒' % (end_time - start_time))
