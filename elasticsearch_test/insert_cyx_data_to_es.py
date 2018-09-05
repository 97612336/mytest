import configparser
import os

import pymysql
from decimal import Decimal
from elasticsearch_dsl import Document, Text, Integer, Date
from elasticsearch_dsl.connections import connections


def get_db_connection():
    home = os.environ['HOME']
    inifile = '{}/.afsaas.cnf'.format(home)
    config = configparser.ConfigParser()
    config.read(inifile)
    user = config.get('client', 'user')
    password = config.get('client', 'password')
    host = config.get('client', 'host')
    config = {
        'host': host,
        'port': 3306,
        'user': user,
        'password': password,
        'db': 'cyx',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }
    connection = pymysql.connect(**config)
    return connection


# 定义类型
# 定义一个文章类
class Articles(Document):
    id = Integer()
    title = Text(analyzer='ik_max_word')
    author_id = Integer()
    atype = Integer()
    publish_time = Date()

    class Index:
        name = 'articles'


# 定义一个用户类
class Users(Document):
    id = Integer()
    username = Text(analyzer='ik_max_word')
    login_at = Date()
    avatar = Text(analyzer='ik_max_word')
    register_time = Date()
    intro = Text(analyzer='ik_max_word')
    utype = Integer()

    class Index:
        name = 'users'


# 定义一个话题类
class Topic(Document):
    id = Integer()
    name = Text(analyzer='ik_max_word')
    intro = Text(analyzer='ik_max_word')
    created_at = Date()

    class Index:
        name = 'topics'


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


# 从数据库中读取用户信息
def read_user_from_sql(n):
    page_size = 30
    db = get_db_connection()
    cursor = db.cursor()
    sql_str = 'select * from users limit %s,%s;' % ((n - 1) * page_size, page_size)
    cursor.execute(sql_str)
    users_res = cursor.fetchall()
    res_list = []
    for one_user in users_res:
        tmp = {}
        tmp['id'] = one_user.get('id')
        tmp['username'] = one_user.get('username')
        tmp['login_at'] = one_user.get('login_at')
        tmp['avatar'] = one_user.get('avatar')
        tmp['register_time'] = one_user.get('created_at')
        tmp['intro'] = one_user.get('intro')
        tmp['utype'] = one_user.get('utype')
        res_list.append(tmp)
    cursor.close()
    db.close()
    return res_list


# 将读取到的用户数据写入到es中
def write_user_to_es(res_list):
    for one_user in res_list:
        u = Users(meta={'id': one_user.get('id')})
        u.id = one_user.get('id')
        u.username = one_user.get('username')
        u.login_at = one_user.get('login_at')
        u.avatar = one_user.get('avatar')
        u.register_time = one_user.get('register_time')
        u.intro = one_user.get('intro')
        u.utype = one_user.get('utype')
        u.save()
        print('成功保存一条用户数据%s' % u.id)


# 从数据库中读取文章信息
def read_article_from_sql(n):
    page_size = 30
    db = get_db_connection()
    cursor = db.cursor()
    sql_str = 'select * from articles limit %s,%s;' % ((n - 1) * page_size, page_size)
    cursor.execute(sql_str)
    articles_res = cursor.fetchall()
    res_list = []
    for one_article in articles_res:
        tmp = {}
        tmp['id'] = one_article.get('id')
        tmp['title'] = one_article.get('title')
        tmp['author_id'] = one_article.get('author_id')
        tmp['atype'] = one_article.get('atype')
        tmp['publish_time'] = one_article.get('created_at')
        res_list.append(tmp)
    cursor.close()
    db.close()
    return res_list


# 将文章信息写入到es中
def write_article_to_es(res_list):
    for one_article in res_list:
        a = Articles(meta={'id': one_article.get('id')})
        a.id = one_article.get('id')
        a.title = one_article.get('title')
        a.author_id = one_article.get('author_id')
        a.atype = one_article.get('atype')
        a.publish_time = one_article.get('publish_time')
        a.save()
        print('成功保存一条文章数据%s' % a.id)


# 从数据库中读取信息到话题信息
def read_topic_from_sql(n):
    page_size = 30
    db = get_db_connection()
    cursor = db.cursor()
    sql_str = 'select * from topics limit %s,%s;' % ((n - 1) * page_size, page_size)
    cursor.execute(sql_str)
    topics_res = cursor.fetchall()
    res_list = []
    for one_topic in topics_res:
        tmp = {}
        tmp['id'] = one_topic.get('id')
        tmp['name'] = one_topic.get('name')
        tmp['intro'] = one_topic.get('intro')
        tmp['created_at'] = one_topic.get('created_at')
        res_list.append(tmp)
    cursor.close()
    db.close()
    return res_list


# 把话题数据写入到es中
def write_topics_to_es(res_list):
    for one_topic in res_list:
        t = Topic(meta={"id": one_topic.get('id')})
        t.id = one_topic.get('id')
        t.name = one_topic.get('name')
        t.intro = one_topic.get('intro')
        t.created_at = one_topic.get('created_at')
        t.save()
        print("保存一条话题数据%s" % t.id)


# 从数据库中读取车型信息
def read_specs_from_sql(n):
    page_size = 30
    db = get_db_connection()
    cursor = db.cursor()
    sql_str = 'select * from specs limit %s,%s;' % ((n - 1) * page_size, page_size)
    cursor.execute(sql_str)
    specs_res = cursor.fetchall()
    res_list = []
    for one_specs in specs_res:
        tmp = {}
        tmp['id'] = one_specs.get('id')
        tmp['series_id'] = one_specs.get('series_id')
        tmp['name'] = one_specs.get('i1')
        price = one_specs.get('i2')
        one_price = str(price).strip('万')
        try:
            new_price = int(Decimal(one_price) * 10000)
        except:
            new_price = None
        tmp['price'] = new_price
        tmp['factory'] = one_specs.get('i3')
        tmp['level'] = one_specs.get('i4')
        res_list.append(tmp)
    cursor.close()
    db.close()
    return res_list


# 写入车型数据到es中
def write_specs_to_es(res_list):
    for one_specs in res_list:
        s = Specs(meta={'id': one_specs.get('id')})
        s.id = one_specs.get('id')
        s.series_id = one_specs.get('series_id')
        s.name = one_specs.get('name')
        s.price = one_specs.get('price')
        s.factory = one_specs.get('factory')
        s.level = one_specs.get('level')
        s.save()
        print('保存了一条车型数据%s' % s.id)


if __name__ == '__main__':
    connections.create_connection(hosts=['127.0.0.1:1235'])
    Users.init()
    Articles.init()
    Topic.init()
    Specs.init()
    i = 1
    while 1:
        has_data = 1
        # 读取用户.存入用户
        users = read_user_from_sql(i)
        if len(users) > 0:
            write_user_to_es(users)
        else:
            print('用户数据已经读写完毕')
            has_data = 0
        # 读取文章,存入文章
        articles = read_article_from_sql(i)
        if len(articles) > 0:
            has_data = 1
            write_article_to_es(articles)
        elif has_data == 0:
            print('文章数据已经读写完毕')
            has_data = 0
        else:
            print('文章数据已经读写完毕')
            has_data = 1
        # 读取话题,存入话题
        topics = read_topic_from_sql(i)
        if len(topics) > 0:
            has_data = 1
            write_topics_to_es(topics)
        elif has_data == 0:
            has_data = 0
            print('话题数据已经读写完毕')
        else:
            has_data = 0
            print('话题数据已经读写完毕')
        # 读取车型,存入车型
        specs = read_specs_from_sql(i)
        if len(specs) > 0:
            has_data = 1
            write_specs_to_es(specs)
        elif has_data == 0:
            has_data = 0
            print('车型数据读写完毕')
        else:
            has_data = 0
            print('车型数据读写完毕')

        if has_data == 0:
            print('所有数据已经读写完毕')
            break
        i = i + 1
