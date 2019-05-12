import time

import pymysql
from elasticsearch import helpers
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections

# get es client
from elasticsearch_dsl.query import MultiMatch


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


# 根据公司的简称，查询公司的全称，并根据全称查找公司的id
def get_company_all_name_by_tmp(invest_adviser_tmp, es, db):
    multi_match = MultiMatch(query=invest_adviser_tmp, fields=['abbreviation'])
    print(invest_adviser_tmp)
    es_res = Search().using(es).index('fullname_and_abbreviation').query(multi_match)
    company_name = ''
    for one in es_res:
        company_name = one.fullname
        break
    # 根据company_name查找公司的id
    sql = 'select id from company where name="%s";' % company_name
    cursor = db.cursor()
    cursor.execute(sql)
    res = cursor.fetchone()
    try:
        company_id = res[0]
    except:
        return 0, ""
    return company_id, company_name


# 获取所有投资经理信息
def get_all_private_manager():
    es = get_es()
    db = get_mysql_db()
    scanResp = helpers.scan(es, scroll="10m", index='private_manager_style', timeout="10m")
    sql_values = ''
    for resp in scanResp:
        name = resp.get('_source').get('touzijingli')
        invest_style = resp.get('_source').get('touzijinglibeijing')
        avg_income = resp.get('_source').get('pingjunshouyi')
        max_income = resp.get('_source').get('zuigaoshouyi')
        min_income = resp.get('_source').get('zuidishouyi')
        range_income = resp.get('_source').get('shouyijicha')
        standard_devi_income = resp.get('_source').get('shouyibiaozhuncha')
        income_ratio = resp.get('_source').get('zhengshouyizhanbi')
        has_produce_num = resp.get('_source').get('zaiguanchanpinzongshu')
        invest_adviser_tmp = resp.get('_source').get('touziguwen')  # 投资顾问简称
        invest_adviser_id, invest_adviser_name = get_company_all_name_by_tmp(invest_adviser_tmp, es, db)
        # 拼接成一个大sql value语句
        sql_values = sql_values + '("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
            name, invest_style, avg_income, max_income, min_income, range_income, standard_devi_income,
            income_ratio, has_produce_num, invest_adviser_name, invest_adviser_id, invest_adviser_tmp
        ) + ','
    sql_values = sql_values[:-1]
    # 执行插入sql的操作
    cursor = db.cursor()
    sql = "insert ignore into private_invest_manager (name,invest_style,avg_income,max_income," \
          "min_income,range_income,standard_devi_income,income_ratio,has_produce_num," \
          "invest_adviser,invest_adviser_id,invest_adviser_shortname) values %s;" % sql_values
    print(sql)
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def run():
    while 1:
        get_all_private_manager()
        print("执行完成，休息一天")
        time.sleep(60 * 60 * 24)


run()
