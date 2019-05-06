from elasticsearch_dsl import connections, Search, Document, Text, Long
from elasticsearch_dsl.query import MultiMatch, Match

es_url = '219.224.134.214:9506'

client = connections.create_connection(hosts=[es_url])

s = Search().using(client).query("match", keyword='8VC')

for hit in s:
    print(hit.keyword)
print('============================')

response = s.execute()
print(response)
print('===============================')
print(s.to_dict())
print('================================')

print(s.count())


# 定义一个私募基金类
class SiMu(Document):
    id = Text()
    establishDate = Long()
    fundName = Text()
    managerName = Text()
    mandatorName = Text()
    putOnRecordDate = Long()

    class Index:
        name = 'simu'


search_words = '第二基金'
simu = SiMu.search()
print(simu)
print(simu.count())
simu_res = simu.query()
print(simu_res.count())
print('========================')

# 总结系统的方法
simu = Search().using(client).query('match', keyword='8VC')
for one in simu:
    print(one)
    print(one.keyword)
    print(one.project)

print('=========================')

# 测试多条件查询，最终完成版
search_words = '第二基金呵呵'
multi_match = MultiMatch(query=search_words, fields=['fundName'])

zhihu = Search().using(client).index('simu').query(multi_match)

for one in zhihu:
    print(one)
    print(one.fundName)
    print(one.id)
    print(one.managerName)