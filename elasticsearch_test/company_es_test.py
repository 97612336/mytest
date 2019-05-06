from elasticsearch_dsl import connections, Document, Text, Long
from elasticsearch_dsl.query import MultiMatch

es_url = '219.224.134.214:9506'

es = connections.create_connection(hosts=[es_url])
print(es)


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


search_words = '基金'
simu = SiMu.search()
multi_match = MultiMatch(query=search_words, fields=['fundName'])
res = simu.query(multi_match)[0:20]
print(res)
for one in res:
    print(one.id)
    print(one.fundName)
