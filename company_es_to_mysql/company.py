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


# 根据金融牌照姓名查找金融牌照的id
def find_finan_kind_id_by_name(kind_name, db):
    sql = 'select id from finan_kind where name="%s";' % (kind_name)
    cursor = db.cursor()
    cursor.execute(sql)
    res = cursor.fetchone()
    finan_kind_id = res[0]
    cursor.close()
    return finan_kind_id


# 插入数据到公司表
def insert_company():
    es = get_es()
    db = get_mysql_db()
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
    # 根据牌照名，查询牌照下的所有公司
    for one_kind_name in new_list:
        # 查询es牌照表中的所有数据
        scanResp = helpers.scan(es, scroll="10m", index='finance_license', timeout="10m",
                                query={"query": {"match": {"license_name": one_kind_name}}})
        # 带插入的sql的values语句
        insert_sql_values = ''
        for resp in scanResp:
            lecense_name = resp.get('_source').get('license_name')
            lecense_id = find_finan_kind_id_by_name(lecense_name, db)
            company_name = resp.get('_source').get('institution_name')
            insert_sql_values = insert_sql_values + '("%s","%s","%s")' % (company_name, lecense_id, lecense_name) + ','
        insert_sql_values = insert_sql_values[:-1]
        # 执行插入数据库的操作
        sql = 'INSERT IGNORE into company (name,finan_kind_id,finan_kind_name) VALUES %s;' % insert_sql_values
        cursor = db.cursor()
        res = cursor.execute(sql)
        print("插入了", res, "行")
        db.commit()
        cursor.close()


# run method
def run_company():
    while 1:
        insert_company()
        print('运行完成，休息一天')
        time.sleep(60 * 60 * 24)


run_company()
