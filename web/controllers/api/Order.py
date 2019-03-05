import json, decimal

from common.libs.UrlManager import UrlManager
from common.libs.member.CartService import CartService
from common.models.food.Food import Food
from common.models.member.Oauth_Member_Bind import OauthMemberBind
from common.models.pay.PayOrder import PayOrder
from web.controllers.api import route_api
from flask import jsonify, request, g
from common.libs.pay.PayService import PayService

@route_api.route("/order/info", methods=['GET', "POST"])
def orderInfo():
    resp = {"code": 200, "msg": "操作成功", "data": {}}
    req = request.values
    params_goods = req.get('goods', None)
    member_info = g.member_info
    params_goods_list = []
    if params_goods:
        params_goods_list = json.loads(params_goods)
    # 定义food_dic 用于存储商品id和数量
    food_dic = {}
    for item in params_goods_list:
        food_dic[item['id']] = item['number']
    food_ids = food_dic.keys()
    food_list = Food.query.filter(Food.id.in_(food_ids)).all()
    data_food_list = []
    yun_price = pay_price = decimal.Decimal(0.00)
    if food_list:
        for item in food_list:
            tmp_data = {
                "id": item.id,
                "name": item.name,
                "price": str(item.price),
                "pic_url": UrlManager.buildImageUrl(item.main_image),
                "number": food_dic[item.id],
            }
            pay_price = pay_price + item.price * int(food_dic[item.id])
            data_food_list.append(tmp_data)
    default_address = {
        "name": "小安",
        "mobile": "1234567890",
        "detail": "河南郑州"
    }
    resp['data']['food_list'] = data_food_list
    resp['data']['pay_price'] = str(pay_price)
    resp['data']['yun_price'] = str(yun_price)
    resp['data']['total_price'] = str(pay_price + yun_price)
    resp['data']['default_address'] = default_address
    return jsonify(resp)


@route_api.route("/order/create", methods=['GET', "POST"])
def orderCreate():
    resp = {"code": 200, "msg": "操作成功", "data": {}}
    req = request.values

    type = req.get('type', '')
    params_goods = req.get('goods', None)
    # 解析数据
    items = []
    if params_goods:
        items = json.loads(params_goods)

    if len(items)<1:
        resp['code'] = -1
        resp['msg'] = '下单失败, 无商品'
        return jsonify(resp)

    member_info = g.member_info
    target = PayService()
    params = {}
    resp = target.createOrder(member_info.id, items, params)
    if resp['code'] == 200 and type =='cart':
        # 删购物车
        CartService.deleteItem(member_info.id, items)
    return jsonify(resp)


@route_api.route("/order/pay", methods=["POST"])
def orderPay():
    resp = {"code": 200, "msg": "操作成功", "data": {}}
    member_info = g.member_info
    req = request.values
    order_sn = req.get("order_sn", '')
    pay_order_info = PayOrder.query.filter_by(order_sn == order_sn).first()
    if not pay_order_info:
        resp['code'] = -1
        resp['msg'] = '系统繁忙'
        return jsonify(resp)
    oauth_bind_info = OauthMemberBind.query.filter_by(member_id = member_info.id).first()
    if not oauth_bind_info:
        resp['code'] = -1
        resp['msg'] = "系统繁忙, 请稍后再试"
        return jsonify(resp)
    return jsonify(resp)






















