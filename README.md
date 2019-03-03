# Python Flask 订餐系统
================
## 启动
       export ops_config=local|production && python manager.py runserver

##flask-sqlacodegen

    flask-sqlacodegen 'mysql+pymysql://root:123456@127.0.0.1/food_db' --outfile "common/models/model.py"  --flask
    flask-sqlacodegen 'mysql+pymysql://root:123456@127.0.0.1/food_db' --tables user --outfile "common/models/user.py"  --flask
    flask-sqlacodegen 'mysql+pymysql://root:123456@127.0.0.1/food_db' --tables food --outfile "common/models/food/Food.py"  --flask
    flask-sqlacodegen 'mysql+pymysql://root:123456@127.0.0.1/food_db' --tables food_cat --outfile "common/models/food/FoodCat.py"  --flask
    flask-sqlacodegen 'mysql+pymysql://root:123456@127.0.0.1/food_db' --tables food_sale_change_log --outfile "common/models/food/FoodSaleChangeLog.py"  --flask
    flask-sqlacodegen 'mysql+pymysql://root:123456@127.0.0.1/food_db' --tables food_stock_change_log --outfile "common/models/food/FoodStockChangeLog.py"  --flask
    flask-sqlacodegen 'mysql+pymysql://root:123456@127.0.0.1/food_db' --tables images --outfile "common/models/image.py"  --flask
    flask-sqlacodegen 'mysql+pymysql://root:123456@127.0.0.1/food_db' --tables pay_order --outfile "common/models/pay/PayOrder.py"  --flask
    flask-sqlacodegen 'mysql+pymysql://root:123456@127.0.0.1/food_db' --tables pay_order_item --outfile "common/models/pay/PayOrderItem.py"  --flask
    flask-sqlacodegen 'mysql+pymysql://root:123456@127.0.0.1/food_db' --tables pay_order_callback_data --outfile "common/models/pay/PayOrderCallbackData"  --flask
