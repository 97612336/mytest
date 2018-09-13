import configparser
import os
import pymysql


# 得到连接数据库的connection
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


# 获取所有车系的车型id
def get_all_specs_series_id():
    db = get_db_connection()
    cursor = db.cursor()
    sql_str = "select DISTINCT(series_id) from specs;"
    cursor.execute(sql_str)
    res = cursor.fetchall()
    specs_series_id_list = []
    for one_series_id in res:
        specs_series_id_list.append(one_series_id.get('series_id'))
    cursor.close()
    db.close()
    return specs_series_id_list


# 根据所有的车系id，筛选出不在series表中的车系id
def get_all_no_series_id(series_id_list):
    db = get_db_connection()
    cursor = db.cursor()
    not_exit_series = []
    for one_series_id in series_id_list:
        sql_str = "select count(1) from series where id=%s" % one_series_id
        cursor.execute(sql_str)
        count_tmp = cursor.fetchone()
        count_num = count_tmp.get('count(1)')
        if count_num == 0:
            not_exit_series.append(one_series_id)
    cursor.close()
    db.close()
    return not_exit_series


# 根据不存在的车系id，写迁移文件
def write_sql_file(not_exit_series):
    for one_series_id in not_exit_series:
        sql_str = 'DELETE from specs WHERE series_id=%s;' % one_series_id
        with open('a.up.sql', 'a+') as f1:
            f1.write(sql_str + '\n')


if __name__ == '__main__':
    all_series_id = get_all_specs_series_id()
    not_exit_series = get_all_no_series_id(all_series_id)
    write_sql_file(not_exit_series)
