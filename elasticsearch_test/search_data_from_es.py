import time
from elasticsearch_dsl import connections
from elasticsearch_dsl import Document, Text, Integer

# 定义一个文档类
from elasticsearch_dsl.query import MultiMatch


class Articles(Document):
    title = Text(analyzer='ik_max_word')
    id = Integer()
    author = Text(analyzer='ik_max_word')
    comment = Text(analyzer='ik_max_word')
    car_name = Text(analyzer='ik_max_word')

    class Index:
        name = 'cyx'


def search_for_es(search_word, n):
    page_size = 20
    connections.create_connection(hosts=['localhost'])
    s = Articles.search()
    mul_math = MultiMatch(query=search_word, fields=['title', 'comment'])
    res = s.query(mul_math)[(n - 1) * page_size:n * page_size]
    for one in res:
        print(one.title)
    connections.remove_connection()

if __name__ == '__main__':
    i = 1
    while 1:
        start_time = time.time()
        search_for_es('汽车', i)
        end_time = time.time()
        i = i + 1
        print('共花费了%s秒' % (end_time - start_time))
