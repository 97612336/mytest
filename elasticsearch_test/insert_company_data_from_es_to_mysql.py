import pymysql
from elasticsearch import helpers
from elasticsearch_dsl import connections, Search


# 获取es链接
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


# 插入数据到金融牌照表
def insert_finan_kind(es, db):
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
    for one_finan_kind in new_list:
        # 进行插入MySQL数据库的操作
        sql = 'INSERT into financial_kind (name) VALUES("%s");' % (one_finan_kind)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()


# 根据金融牌照姓名查找金融牌照的id
def find_finan_kind_id_by_name(kind_name, db):
    sql = 'select id from financial_kind where name="%s";' % (kind_name)
    cursor = db.cursor()
    cursor.execute(sql)
    res = cursor.fetchone()
    finan_kind_id = res[0]
    cursor.close()
    return finan_kind_id


# 插入该牌照下的所有公司信息到公司表中
def insert_into_mysql_by_kind_name(kind_name, db):
    # 查询es牌照表中的所有数据
    scanResp = helpers.scan(es, scroll="10m", index='finance_license', timeout="10m",
                            query={"query": {"match": {"license_name": kind_name}}})
    i = 1
    for resp in scanResp:
        lecense_name = resp.get('_source').get('license_name')
        lecense_id = find_finan_kind_id_by_name(lecense_name, db)
        company_name = resp.get('_source').get('institution_name')
        # 执行存入数据库的操作
        cursor = db.cursor()
        sql = 'INSERT into company (name,finan_kind_id,finan_kind_name) VALUES("%s","%s","%s");' % (
            company_name, lecense_id, lecense_name)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        i = i + 1
    print(i)


# 插入数据到公司表
def insert_company(es, db):
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
        insert_into_mysql_by_kind_name(one_kind_name, db)


if __name__ == '__main__':
    db = get_mysql_db()
    es = get_es()
    # 插入十八种金融牌照的数据
    # insert_finan_kind(es, db)
    # 插入公司信息
    insert_company(es, db)
