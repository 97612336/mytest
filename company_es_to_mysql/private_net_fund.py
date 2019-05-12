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


def get_company_id_by_name(company_name, db):
    sql = 'select id from company where name="%s";' % (company_name)
    cursor = db.cursor()
    cursor.execute(sql)
    res = cursor.fetchone()
    try:
        finan_kind_id = res[0]
    except:
        return ''
    finally:
        cursor.close()
    return finan_kind_id


def get_invest_manger_id_by_name(invest_manager, db):
    cursor = db.cursor()
    sql = 'select id from private_invest_manager where name="%s";' % invest_manager
    cursor.execute(sql)
    res = cursor.fetchone()
    try:
        manager_id = res[0]
    except:
        return 0
    finally:
        cursor.close()
    return manager_id


def get_all_private_net_fund_info():
    es = get_es()
    db = get_mysql_db()
    # 查询es牌照表中的所有数据
    scanResp = helpers.scan(es, scroll="10m", index='private_net_value', timeout="10m")
    i = 1
    sql_values = ''
    for resp in scanResp:
        fund_id = resp.get('_source').get('daima')
        name = resp.get('_source').get('jiancheng')
        company_name = resp.get('_source').get('touziguwen')
        company_id = get_company_id_by_name(company_name, db)
        new_data = resp.get('_source').get('zuixin_riqi')
        now_netasset_value = resp.get('_source').get('zuixin_danweijingzhi')
        fuquan_value = resp.get('_source').get('zuixin_fuquandanweijingzhi')
        leiji_value = resp.get('_source').get('zuixin_leijidanweijingzhi')
        increase_ratio = resp.get('_source').get('zuixin_zengchanglv')
        before_data = resp.get('_source').get('shangqi_riqi')
        before_netasset_value = resp.get('_source').get('shangqi_danweijingzhi')
        close_year_return = resp.get('_source').get('jinnianyilai_zonghuibao')
        close_year_ranking = resp.get('_source').get('jinnianyilai_tongleipaiming')
        one_month_return = resp.get('_source').get('zuijinyiyue_zonghuibao')
        three_month_return = resp.get('_source').get('zuijinsanyue_zonghuibao')
        six_month_return = resp.get('_source').get('zuijinliuyue_zonghuibao')
        one_year_return = resp.get('_source').get('zuijinyinian_zonghuibao')
        one_year_ranking = resp.get('_source').get('zuijinyinian_tongleipaiming')
        two_year_return = resp.get('_source').get('zuijinliangnian_zonghuibao')
        two_year_ranking = resp.get('_source').get('zuijinliangnian_tongleipaiming')
        three_year_return = resp.get('_source').get('zuijinsannian_zonghuibao')
        three_year_ranking = resp.get('_source').get('zuijinsannian_tongleipaiming')
        all_return = resp.get('_source').get('chengliyilai_zonghuibao')
        scale = resp.get('_source').get('faxingguimo')
        estblish = resp.get('_source').get('chengliriqi')
        invest_type = resp.get('_source').get('touzileixing')
        concept = resp.get('_source').get('suoshugainian')
        is_structured = resp.get('_source').get('shifoujiegouhua')
        invest_manager = resp.get('_source').get('touzijingli')  # 投资经理
        # invest_manager_id = resp.get('_source').get('')  # 等待经理表插入完成
        trust_company = resp.get('_source').get('xintuogongsi')
        custodian = resp.get('_source').get('tuoguanren')
        broker_company = resp.get('_source').get('zhengquanjingjiren')
        invest_manager_id = get_invest_manger_id_by_name(invest_manager, db)
        print(company_name)
        print(company_id)
        print(broker_company)
        sql_values = sql_values + '("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
            fund_id, name, company_id, company_name, new_data, now_netasset_value, fuquan_value, leiji_value,
            increase_ratio, before_data, before_netasset_value, close_year_return, close_year_ranking,
            one_month_return, three_month_return, six_month_return, one_year_return,
            one_year_ranking, two_year_return, two_year_ranking, three_year_return, three_year_ranking,
            all_return, scale, estblish, invest_type, concept, is_structured, invest_manager, invest_manager_id,
            trust_company, custodian, broker_company
        ) + ','
        i = i + 1
    sql_values = sql_values[:-1]
    # 执行插入MySQL的操作
    cursor = db.cursor()
    sql = 'insert ignore into private_net_fund (fund_id,name,company_id,company_name,new_date,now_netasset_value,' \
          'fuquan_value,leiji_value,increase_ratio,before_date,before_netasset_value,close_year_return,' \
          'close_year_ranking,one_month_return,three_month_return,six_month_return,one_year_return,one_year_ranking,' \
          'two_year_return,two_year_ranking,three_year_return,three_year_ranking,all_return,scale,estblish,invest_type,' \
          'concept,is_structured,invest_manager,invest_manager_id,trust_company,custodian,broker_company) values ' + \
          sql_values + ';'
    print(sql)
    print(sql_values)
    print(i)
    lines = cursor.execute(sql)
    db.commit()
    print('共插入了', lines, '行')


def run():
    while 1:
        get_all_private_net_fund_info()
        print('执行完成，休息一天')
        time.sleep(60 * 60 * 24)


run()
