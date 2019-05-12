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


# 先获取所有的公司，然后根据公司名称去搜索新闻，如果匹配就保存到数据库中
def get_all_company_dict(db):
    sql = "select id,name from company;"
    cursor = db.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    company_name_list = []
    for one in res:
        tmp = {}
        tmp['company_id'] = one[0]
        tmp['company_name'] = one[1]
        company_name_list.append(tmp)
    return company_name_list


# 根据一个公司名去查询新闻表中关于该公司的新闻
def get_finan_kind_by_company_id(company_id, db):
    cursor = db.cursor()
    sql = 'select finan_kind_id from company_finan_kind where company_id="%s";' % company_id
    cursor.execute(sql)
    finan_kind_id = cursor.fetchone()[0]
    return finan_kind_id


def get_news_by_company_name(company_dict, db):
    es = get_es()
    # 查询和讯的信息
    hexun_sql = ''
    multi_match = MultiMatch(query=company_dict.get('company_name'), fields=['content'])
    hexun = Search().using(es).index('hexun').query(multi_match)
    for one in hexun:
        company_id = company_dict.get('company_id')
        company_name = company_dict.get('company_name')
        try:
            publish_time = one.date
        except:
            break
        title = one.title
        source = one.source
        if source == '':
            source = '和讯'
        content = one.content
        link = one.url
        finan_kind = get_finan_kind_by_company_id(company_id, db)
        hexun_sql = hexun_sql + '("%s","%s","%s","%s","%s","%s","%s","%s")' % (
            company_id, company_name, publish_time, pymysql.escape_string(title), source,
            pymysql.escape_string(content), link, finan_kind) + ','
    hexun_sql = hexun_sql[:-1]
    # 中国融资租赁资源网
    flleasing_sql = ''
    multi_match2 = MultiMatch(query=company_dict.get('company_name'), fields=['content'])
    flleasing = Search().using(es).index('flleasing').query(multi_match2)
    for one in flleasing:
        company_id = company_dict.get('company_id')
        company_name = company_dict.get('company_name')
        try:
            publish_time = one.date
        except:
            break
        title = one.title
        source = one.source
        if source == '':
            source = '中国融资租赁资源网'
        content = one.content
        link = one.url
        finan_kind = get_finan_kind_by_company_id(company_id, db)
        flleasing_sql = flleasing_sql + '("%s","%s","%s","%s","%s","%s","%s","%s")' % (
            company_id, company_name, publish_time, pymysql.escape_string(title), source,
            pymysql.escape_string(content), link, finan_kind) + ','
    flleasing_sql = flleasing_sql[:-1]
    # 中国融资担保业协会
    chinafga_sql = ''
    multi_match3 = MultiMatch(query=company_dict.get('company_name'), fields=['content'])
    chinafga = Search().using(es).index('chinafga').query(multi_match3)
    for one in chinafga:
        company_id = company_dict.get('company_id')
        company_name = company_dict.get('company_name')
        try:
            publish_time = one.date
        except:
            break
        title = one.title
        source = one.source
        if source == '':
            source = '中国融资担保业协会'
        content = one.content
        link = one.url
        finan_kind = get_finan_kind_by_company_id(company_id, db)
        chinafga_sql = chinafga_sql + '("%s","%s","%s","%s","%s","%s","%s","%s")' % (
            company_id, company_name, publish_time, pymysql.escape_string(title), source,
            pymysql.escape_string(content), link, finan_kind) + ','
    chinafga_sql = chinafga_sql[:-1]
    # 网贷天眼新闻
    wdty_sql = ""
    multi_match4 = MultiMatch(query=company_dict.get('company_name'), fields=['content'])
    wdty = Search().using(es).index('chinafga').query(multi_match4)
    for one in wdty:
        company_id = company_dict.get('company_id')
        company_name = company_dict.get('company_name')
        try:
            publish_time = one.news_publish_dt
        except:
            break
        title = one.news_title
        source = one.news_source
        if source == '':
            source = '网贷天眼新闻'
        content = one.news_content
        link = one.news_url
        finan_kind = get_finan_kind_by_company_id(company_id, db)
        wdty_sql = wdty_sql + '("%s","%s","%s","%s","%s","%s","%s","%s")' % (
            company_id, company_name, publish_time, pymysql.escape_string(title), source,
            pymysql.escape_string(content), link, finan_kind) + ','
    wdty_sql = wdty_sql[:-1]
    # 总的sql返回
    all_sql_list = []
    all_sql_list.append(hexun_sql)
    all_sql_list.append(flleasing_sql)
    all_sql_list.append(chinafga_sql)
    all_sql_list.append(wdty_sql)
    return all_sql_list


# 执行sql插入语句
def insert_data(values_sql_list, db):
    cursor = db.cursor()
    for one_sql in values_sql_list:
        if not one_sql:
            break
        sql = "insert ignore into company_news (company_id,company_name,publish_time,title,source,content,link,finan_kind) values %s;" % one_sql
        print(sql)
        line_num = cursor.execute(sql)
        db.commit()
        print('共插入', line_num, '行')
    cursor.close()


def run():
    while 1:
        db = get_mysql_db()
        company_dict_list = get_all_company_dict(db)
        print(len(company_dict_list))
        for one_dict in company_dict_list:
            values_sql_list = get_news_by_company_name(one_dict, db)
            insert_data(values_sql_list, db)
        print("执行完成，休息一天")
        time.sleep(60 * 60 * 24)


run()
