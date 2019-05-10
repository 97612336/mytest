import pymysql
from celery import Celery

app = Celery('hello', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


@app.task
def insert_data(name):
    conf_dict = {
        'SqlHost': '127.0.0.1',
        'SqlPort': 3306,
        'SqlUser': 'root',
        'SqlPassword': 'root123456',
    }
    db = pymysql.connect(host=conf_dict.get("SqlHost"), port=int(conf_dict.get("SqlPort")),
                         user=conf_dict.get("SqlUser"), password=conf_dict.get("SqlPassword"),
                         db="test_celery", charset='utf8mb4')
    cursor = db.cursor()
    sql = 'insert into test (id,name) value(1,"%s");' % name
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
