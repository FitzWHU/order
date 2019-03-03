from web.controllers.api import route_api
from flask import request, jsonify, g
from common.models.food.Food import Food
from application import app, db
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem
from common.libs.UrlManager import UrlManager
from common.libs.Helper import selectFilterObj, getDictFilterField, getCurrentData
# from common.models.member.MemberComments import MemberComments
import json, datetime


@route_api.route("/my/order")
def myOrderList():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    member_info = g.member_info
    req = request.values
    status = int(req['status']) if 'status' in req else 0
    # 查询用户所有的订单 判断状态返回相应数据
    query = PayOrder.query.filter_by(member_id=member_info.id)
    if status == -8:  # 等待付款
        query = query.filter(PayOrder.status == -8)
    elif status == -7:  # 待发货
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == -7, PayOrder.comment_status == 0)
    elif status == -6:  # 待确认
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == -6, PayOrder.comment_status == 0)
    elif status == -5:  # 待评价
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == 1, PayOrder.comment_status == 0)
    elif status == 1:  # 已完成
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == 1, PayOrder.comment_status == 1)
    else:
        query = query.filter(PayOrder.status == 0)
    # 查询用户相应的订单
    pay_order_list = query.order_by(PayOrder.id.desc()).all()
    # 定义一个列表 用于存储订单的信息
    data_pay_order_list = []
    if pay_order_list:
        # 得到所有订单的id ex: [1, 2, 3]
        pay_order_ids = selectFilterObj(pay_order_list, "id")
        print(pay_order_ids)
        # 查询所有订单所对应的商品
        pay_order_item_list = PayOrderItem.query.filter(PayOrderItem.pay_order_id.in_(pay_order_ids)).all()
        print(pay_order_item_list)
        # 得到所有商品的信息id
        food_ids = selectFilterObj(pay_order_item_list, "food_id")
        # 得到
        food_map = getDictFilterField(Food, Food.id, "id", food_ids)
        print(food_map)
        # 定义一个字典  {订单id:[{商品信息1},{商品信息2}], ........}
        pay_order_item_map = {}
        if pay_order_item_list:
            for item in pay_order_item_list:
                # 初始化
                if item.pay_order_id not in pay_order_item_map:
                    pay_order_item_map[item.pay_order_id] = []
                # 得到商品的信息
                tmp_food_info = food_map[item.food_id]

                pay_order_item_map[item.pay_order_id].append({
                    'id': item.id,
                    'food_id': item.food_id,
                    'quantity': item.quantity,
                    'price': str(item.price),
                    'pic_url': UrlManager.buildImageUrl(tmp_food_info.main_image),
                    'name': tmp_food_info.name
                })

        for item in pay_order_list:
            tmp_data = {
                'status': item.pay_status,
                'status_desc': item.status_desc,
                'date': item.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                'order_number': item.order_number,
                'order_sn': item.order_sn,
                'note': item.note,
                'total_price': str(item.total_price),
                'goods_list': pay_order_item_map[item.id]
            }

            data_pay_order_list.append(tmp_data)
    resp['data']['pay_order_list'] = data_pay_order_list
    return jsonify(resp)
