import time

import pymysql
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
        'SqlHost': '219.224.134.214',
        'SqlPort': 3307,
        'SqlUser': 'root',
        'SqlPassword': 'mysql3307',
    }
    conn = pymysql.connect(host=conf_dict.get("SqlHost"), port=int(conf_dict.get("SqlPort")),
                           user=conf_dict.get("SqlUser"), password=conf_dict.get("SqlPassword"),
                           db="finan", charset='utf8mb4')
    return conn


def run_finan_kind():
    db = get_mysql_db()
    es = get_es()
    while 1:
        # 去重查询hexun表相应的字段
        fl = Search().using(es).index("finance_license")
        fl.aggs.bucket('one_kind', 'terms', field="license_name.keyword", size=1000)
        response = fl.execute()
        finan_licen_list = []
        for one in response.aggregations.one_kind.buckets:
            # 单个的不重复的值
            finan_licen_list.append(one.key)
        # 过滤数据
        new_list = []
        for one in finan_licen_list:
            if one != '':
                new_list.append(one)
        print(new_list)
        for one_finan_kind in new_list:
            # 进行插入MySQL数据库的操作
            sql = 'INSERT into finan_kind (name) VALUES("%s");' % (one_finan_kind)
            cursor = db.cursor()
            try:
                cursor.execute(sql)
                db.commit()
            except:
                pass
            cursor.close()
        print('金融牌照表的数据已经插入完成，休息24小时')
        time.sleep(60 * 60 * 24)


run_finan_kind()
