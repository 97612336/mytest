from elasticsearch_dsl import Document, connections, Text
from elasticsearch_dsl.query import MultiMatch

es = connections.create_connection()


# 定义一个私募基金类
class Sisi(Document):
    id = Text()
    name = Text()
    desc = Text()

    class Index:
        name = 'sisi'


sisi = Sisi().search()
mul_math = MultiMatch(query='hahah', fields=['name'])
res = sisi.query(mul_math)
for one in res:
    print(one)
    print(one.id)
    print(one.name)
    print(one.desc)

print('==============================')


