import configparser
import os

import pymysql
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
        'db': 'cheyixiao',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }
    connection = pymysql.connect(**config)
    return connection


# 定义一个文档类
class Articles(Document):
    title = Text(analyzer='ik_max_word')
    body = Text(analyzer='ik_max_word')
    lines = Integer()

    class Index:
        name = 'test'


if __name__ == '__main__':
    connections.create_connection(hosts=['localhost'])
    db = get_db_connection()
    Articles.init()
    article = Articles(meta={'id': 8}, title='这是标题2', body='这是文章体2')
    article.save()
