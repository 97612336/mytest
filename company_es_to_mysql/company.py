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
        'SqlHost': '219.224.134.214',
        'SqlPort': 3307,
        'SqlUser': 'root',
        'SqlPassword': 'mysql3307',
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


def get_company_id_by_name(company_name, db):
    sql = 'select id from company where name="%s";' % (company_name)
    cursor = db.cursor()
    cursor.execute(sql)
    res = cursor.fetchone()
    try:
        company_id = res[0]
    except:
        return ''
    finally:
        cursor.close()
    return company_id


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
    print(new_list)
    for one_kind_name in new_list:
        # 查询es牌照表中的所有数据
        scanResp = helpers.scan(es, scroll="10m", index='finance_license', timeout="10m",
                                query={"query": {"match": {"license_name": one_kind_name}}})
        # 带插入的sql的values语句
        insert_sql_values1 = ''
        print(one_kind_name)
        for resp in scanResp:
            company_name = resp.get('_source').get('institution_name')
            company_code = resp.get('_source').get('institution_code')
            print(company_name)
            insert_sql_values1 = insert_sql_values1 + '("%s","%s")' % (company_code, company_name) + ','
        insert_sql_values1 = insert_sql_values1[:-1]
        # 执行插入数据库的操作
        sql = 'INSERT IGNORE into company (company_code,name) VALUES %s;' % insert_sql_values1
        cursor = db.cursor()
        res = cursor.execute(sql)
        print("插入了", res, "行")
        db.commit()
        cursor.close()


# 插入数据到公司和金融牌照的关联表中
def insert_into_company_finan_kind():
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
    print(new_list)
    for one_kind_name in new_list:
        # 查询es牌照表中的所有数据
        scanResp = helpers.scan(es, scroll="10m", index='finance_license', timeout="10m",
                                query={"query": {"match": {"license_name": one_kind_name}}})
        # 带插入的sql的values语句
        insert_sql_values = ''
        print(one_kind_name)
        for resp in scanResp:
            finan_kind_name = resp.get('_source').get('license_name')
            finan_kind_id = find_finan_kind_id_by_name(finan_kind_name, db)
            company_name = resp.get('_source').get('institution_name')
            company_id = get_company_id_by_name(company_name, db)
            print(company_name)
            insert_sql_values = insert_sql_values + '("%s","%s","%s","%s")' % (
                company_id, company_name, finan_kind_id, finan_kind_name) + ','
        insert_sql_values = insert_sql_values[:-1]
        # 执行插入数据库的操作
        sql = 'INSERT IGNORE into company_finan_kind (company_id,company_name,finan_kind_id,finan_kind_name) VALUES %s;' % insert_sql_values
        cursor = db.cursor()
        res = cursor.execute(sql)
        print("插入了", res, "行")
        db.commit()
        cursor.close()


# run method
def run_company():
    print("开始执行")
    while 1:
        insert_company()
        print('公司表插入完成')
        time.sleep(5)
        print("开始插入公司和金融牌照关联表")
        insert_into_company_finan_kind()
        print('运行完成，休息一天')
        time.sleep(60 * 60 * 24)


run_company()
