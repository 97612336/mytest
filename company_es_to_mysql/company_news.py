import time

import pymysql
from elasticsearch import helpers
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections


# get es client
def get_es():
    es_url = '219.224.134.214:9506'
    client = connections.create_connection(hosts=[es_url])
    return client


# 获取mysql的链接
def get_mysql_db():
    conf_dict = {
        'SqlHost': '127.0.0.1',
        'SqlPort': 3306,
        'SqlUser': 'root',
        'SqlPassword': 'root123456',
    }
    conn = pymysql.connect(host=conf_dict.get("SqlHost"), port=int(conf_dict.get("SqlPort")),
                           user=conf_dict.get("SqlUser"), password=conf_dict.get("SqlPassword"),
                           db="finan", charset='utf8mb4')
    return conn


