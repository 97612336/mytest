import os

from elasticsearch_dsl import Document, Integer, Text, Date, connections
from elasticsearch_dsl.query import MultiMatch

es_ip = os.getenv('ES_IP', '127.0.0.1')
connections.create_connection(hosts=[es_ip])


class Articles(Document):
    id = Integer()
    title = Text(analyzer='ik_max_word')
    title_pinyin = Text(analyzer='pinyin')
    author_id = Integer()
    atype = Integer()
    publish_time = Date()

    class Index:
        name = 'articles'


def get_high_title(one_str):
    one_art_title = []
    hig_str_list = str(one_str).split("<em>")
    for one_str in hig_str_list:
        if "</em>" not in one_str:
            tmp = {}
            tmp['type'] = 0
            tmp['content'] = one_str
            one_art_title.append(tmp)
        else:
            tmp_list = one_str.split('</em>')
            tmp1 = {}
            tmp1['type'] = 1
            tmp1['content'] = tmp_list[0]
            tmp2 = {}
            tmp2['type'] = 0
            tmp2['content'] = tmp_list[1]
            one_art_title.append(tmp1)
            one_art_title.append(tmp2)
    return one_art_title


art = Articles.search()
art_mul = MultiMatch(query="文章实例", fields=['title', 'title_pinyin'])
art_res = art.query(art_mul).highlight('title')[0:3]
for one_art in art_res:
    print(one_art.id)
    # 获取高亮部分带<em>标签的值
    highlight = one_art.meta.highlight.title[0]
    one_list = get_high_title(highlight)
    print(one_list)
