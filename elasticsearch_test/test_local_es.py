from elasticsearch_dsl import Document, connections, Text

es = connections.create_connection()


# 定义一个私募基金类
class Sisi(Document):
    id = Text()
    name = Text()
    desc = Text()

    class Index:
        name = 'sisi'


Sisi().init()

id = 1
name = 'hahah'
desc = 'this is a desc'

one_sisi = Sisi(meta={'id': id})
one_sisi.id = id
one_sisi.name = name
one_sisi.desc = desc
one_sisi.save()

