# Python Flask 订餐系统
================
## 启动
       export ops_config=local|production && python manager.py runserver

##flask-sqlacodegen

    flask-sqlacodegen 'mysql+pymysql://root:123456@127.0.0.1/food_db' --outfile "common/models/model.py"  --flask
    flask-sqlacodegen 'mysql+pymysql://root:123456@127.0.0.1/food_db' --tables user --outfile "common/models/user.py"  --flask