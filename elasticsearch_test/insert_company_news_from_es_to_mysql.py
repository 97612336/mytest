# 获取es链接
import pymysql
from elasticsearch import helpers
from elasticsearch_dsl.connections import connections


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


es = get_es()
db = get_mysql_db()

# 查询es牌照表中的所有数据
scanResp = helpers.scan(es, scroll="10m", index='finance_license', timeout="10m",
                        query={"query": {"match": {"license_name": '私募'}}})
i = 1
for resp in scanResp:
    lecense_name = resp.get('_source').get('license_name')
    company_name = resp.get('_source').get('institution_name')
    print(lecense_name)
    print(company_name)
    i = i + 1
print(i)
