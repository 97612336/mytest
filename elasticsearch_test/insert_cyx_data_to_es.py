import configparser
import os

import pymysql
from decimal import Decimal

import time
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
def read_user_from_sql(one_id):
    page_size = 500
    db = get_db_connection()
    cursor = db.cursor()
    sql_str = 'select * from users where id>%s limit %s;' % (one_id, page_size)
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
def read_article_from_sql(last_id):
    page_size = 500
    db = get_db_connection()
    cursor = db.cursor()
    sql_str = 'select * from articles where id>%s limit %s;' % (last_id, page_size)
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
def read_topic_from_sql(last_id):
    page_size = 500
    db = get_db_connection()
    cursor = db.cursor()
    sql_str = 'select * from topics where id>%s limit %s;' % (last_id, page_size)
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
def read_specs_from_sql(last_id):
    page_size = 500
    db = get_db_connection()
    cursor = db.cursor()
    sql_str = 'select * from specs where id>%s limit %s;' % (last_id, page_size)
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


# 对比es中的数据和数据库中的数据的个数
def can_do_insert(sql_table_name, es_model):
    db = get_db_connection()
    cursor = db.cursor()
    sql_str = 'select count(1) from %s;' % sql_table_name
    cursor.execute(sql_str)
    sql_count_num = cursor.fetchone().get('count(1)')
    es_count_num = es_model.search().count()
    cursor.close()
    db.close()
    if sql_count_num > es_count_num:
        s = es_model.search().sort({'id': {'order': 'desc'}})[0:1]
        last_id = 0
        for one in s:
            last_id = one.id
        return last_id
    else:
        return ''


if __name__ == '__main__':
    connections.create_connection(hosts=['127.0.0.1:1235'])
    Users.init()
    Articles.init()
    Topic.init()
    Specs.init()
    while 1:
        start_time = time.time()
        # 判断是否可以插入用户数据
        last_user_id = can_do_insert('users', Users)
        if last_user_id != '':
            # 当do_user是数字的时候,就从这个id往后插入
            user_res = read_user_from_sql(last_user_id)
            write_user_to_es(user_res)
        # 判断是否可以插入文章数据
        last_article_id = can_do_insert('articles', Articles)
        if last_article_id != '':
            # 当do_article是数字的时候,就从这个id往后插入
            article_res = read_article_from_sql(last_article_id)
            write_article_to_es(article_res)
        # 判断是否可以插入话题数据
        last_topics_id = can_do_insert('topics', Topic)
        if last_topics_id != '':
            # 当do_topics是数字的时候,就从这个id往后插入
            topics_res = read_topic_from_sql(last_topics_id)
            write_topics_to_es(topics_res)
        # 判断是否可以插入车型数据
        last_specs_id = can_do_insert('specs', Specs)
        if last_specs_id != '':
            # 当do_specs是数字的时候,就从这个id往后插入
            specs_res = read_specs_from_sql(last_specs_id)
            write_specs_to_es(specs_res)
        end_time = time.time()
        print('本次更新共花费了%s秒' % (end_time - start_time))
        print('休息5分钟...')
        time.sleep(60 * 5)

