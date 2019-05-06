from flask import Flask
import pymysql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import Session as db_session

pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root123456@127.0.0.1:3306/test_mine'
db = SQLAlchemy(app)

# 反向生成模型类
metadata = MetaData()
engine = create_engine(
    'mysql+mysqlconnector://root:root123456@127.0.0.1:3306/test_mine',
    echo=True
)
# 反向生成单表
Date_list = Table('date_list', metadata, autoload=True, autoload_with=engine)
session = db_session(engine)


@app.route('/', methods=['GET'])
def index():
    res = session.query(Date_list).first()
    res_id = res.id
    plat_date = res.plat_date
    return "hello%s,%s" % (res_id, plat_date)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
