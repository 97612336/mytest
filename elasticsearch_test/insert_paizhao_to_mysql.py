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

print(conn)


# 根据牌照名字把数据插入到financial_kind中去
def insert_data(paizhao_name):
    sql = 'INSERT into financial_kind (name) VALUES("%s");' % paizhao_name
    print(sql)
    cursor = conn.cursor()
    res = cursor.execute(sql)
    print(res)
    conn.commit()
    cursor.close()


paizhao = Search().using(es).index('paizhao')
paizhao.aggs.bucket('one_kind', 'terms', field='paizhao_name.keyword')
response = paizhao.execute()
for one in response.aggregations.one_kind.buckets:
    # 单个的不重复的值
    print(one.key)
    paizhao_name = one.key
    res_name = str(paizhao_name).strip()
    print(res_name)
    insert_data(res_name)
