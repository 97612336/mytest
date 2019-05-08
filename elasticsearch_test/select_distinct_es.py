from elasticsearch_dsl import connections, Search

es_url = '219.224.134.214:9506'

es = connections.create_connection(hosts=[es_url])

# 去重查询hexun表相应的字段
hexun = Search().using(es).index("private_net_value")
hexun.aggs.bucket('one_kind', 'terms', field="suoshugainian.keyword")
response = hexun.execute()
for one in response.aggregations.one_kind.buckets:
    # 单个的不重复的值
    print(one.key)
    # 这个值出现的次数
    print(one.doc_count)

print('================================')
