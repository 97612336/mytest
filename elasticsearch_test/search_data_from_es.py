import time
from elasticsearch_dsl import connections
from elasticsearch_dsl import Document, Text, Integer

# 定义一个文档类
from elasticsearch_dsl.query import MultiMatch


# 定义一个车型类
class Specs(Document):
    id = Integer()
    series_id = Integer()
    name = Text(analyzer='ik_max_word')
    price = Integer()
    factory = Text(analyzer='ik_max_word')
    level = Text(analyzer='ik_max_word')

    class Index:
        name = 'specs'


def search_for_es(search_word, n):
    page_size = 20
    connections.create_connection(hosts=['localhost:1235'])
    s = Specs.search()
    mul_math = MultiMatch(query=search_word, fields=['name', 'factory'])
    res = s.query(mul_math)[(n - 1) * page_size:n * page_size]
    for one in res:
        print(one.name)


if __name__ == '__main__':
    i = 1
    start_time = time.time()
    search_for_es('宝马', i)
    end_time = time.time()
    i = i + 1
    print('共花费了%s秒' % (end_time - start_time))
