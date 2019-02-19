from flask import Flask, url_for
from UrlManager import *

from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
# 管理
from flask_migrate import Migrate, MigrateCommand
# 处理App和db之间的关系 / 迁移指令
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql+pymysql://root:123456@localhost:3306/order'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

# 创建Ｍａｎａｇｅｒ对象并制定要管理哪个应用
manager= Manager(app)
# 创建Ｍｉｇｒａｔｅ对象，制定要关联的ＡＰＰ和ｄｂ
migrate = Migrate(app, db)
# 为Ｍａｎａｇｅｒ添加命令，　允许数据迁移
manager.add_command("db", MigrateCommand)


@app.route('/')
def hello_world():
    url = url_for("index")
    url_1 = UrlManager.buildUrl('/api')
    url_2 = UrlManager.buildStaticurl("/css/bootstrap.css")
    msg = 'Hello World!url: %s, url_1: %s, url_2:%s' %(url, url_1, url_2)
    app.logger.error(msg)
    return msg


@app.errorhandler(404)
def page_note_found(error):
    app.logger.error(error)
    return 'This page does not found', 404


@app.route("/index")
def index():
    return "这是主页"

if __name__ == '__main__':
    app.run(debug=True)
