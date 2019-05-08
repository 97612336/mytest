import pymysql
from elasticsearch_dsl import connections, Search

# 配置es
es_url = '219.224.134.214:9506'

es = connections.create_connection(hosts=[es_url])

# 配置mysql
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'root123456'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'test_mine'
conn = pymysql.connect(
    host=HOST,
    user=USERNAME,
    password=PASSWORD,
    database=DATABASE,
    charset='utf8'
)


# 根据牌照名称从ES中查询数据的方法
def get_company_by_paizhao_name(paizhao_name):
    companys_search = Search().using(es).index('paizhao').query('match', paizhao_name=paizhao_name)
    count_num = companys_search.count()
    print(count_num)
    companys = companys_search[0:count_num]
    for one_company in companys:
        print(one_company.jigouquancheng)


# 首先从mysql中读取金融牌照的名称，然后查询ES中相关牌照的公司，然后保存到数据库中
cursor = conn.cursor()
paizhao_name_sql = "select name from financial_kind;"
cursor.execute(paizhao_name_sql)
paizhao_name_res = cursor.fetchall()
for one_paizhao_name_trup in paizhao_name_res:
    paizhao_name = one_paizhao_name_trup[0]
    get_company_by_paizhao_name(paizhao_name)
