from elasticsearch import helpers

# 配置es
from elasticsearch_dsl import connections, Search

es_url = '219.224.134.214:9506'

es = connections.create_connection(hosts=[es_url])

# 查询表中的所有数据
scanResp = helpers.scan(es, scroll="10m", index='paizhao', timeout="10m",
                        query={"query": {"match": {"paizhao_name": "银行（含民营）"}}})

i = 0
for resp in scanResp:
    print(resp.get('_source').get('jigouquancheng'))
    i = i + 1
print(i)

paizhao_res = Search().using(es).index('paizhao')

print(paizhao_res.count())

one_dict = {'_index': 'paizhao', '_type': 'text', '_id': '80711720', '_score': None,
            '_source': {'jigoudaima': 80711720, 'jigouquancheng': '固安恒升村镇银行股份有限公司', 'paizhao_name': '银行（含民营）'},
            'sort': [5587]}

print('====================')

res1 = Search().using(es).index('private_net_value').query('match', touziguwen="深圳东方港湾投资管理股份有限公司")
print(res1.count())

res2 = Search().using(es).index('private_net_value')
print(res2.count())
print('==========================')

one_str = '南京璟恒投资管理有限公司'
res3 = Search().using(es).index('paizhao').query('match', jigouquancheng=one_str)
print(res3.count())
for one in res3:
    print(one)
