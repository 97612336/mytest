import os

import click
import pymysql
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CHAR, Column, Enum, Float, ForeignKey, String, DECIMAL, TEXT
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT, TIMESTAMP, TINYINT, SET, DATETIME, MEDIUMTEXT

app = Flask(__name__)

# 数据库相关配置
db = SQLAlchemy(app)
pymysql.install_as_MySQLdb()
prefix = "mysql://root@127.0.0.1/training"
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# 数据库的模型类
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(INTEGER(11), primary_key=True)
    username = db.Column(CHAR(20), nullable=False, server_default='手机号')
    password = db.Column(CHAR(20), nullable=False, server_default='密码')
    height = db.Column(DECIMAL(5, 2))
    weight = db.Column(DECIMAL(5, 2))
    birthday = db.Column(DATETIME(6))
    sex = db.Column(Enum('female', 'male'))


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(INTEGER(11), primary_key=True)
    name = db.Column(CHAR(20))
    title = db.Column(String(256))


admin = Admin(app, name='后台管理系统', template_mode='bootstrap3')


class AdminModelView(ModelView):
    def is_accessible(self):
        return False


admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Post, db.session))
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
        print("Droped database")
        return
    db.create_all()
