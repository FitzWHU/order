import json

from flask import jsonify, request, g

from common.libs.UrlManager import UrlManager
from common.libs.member.CartService import CartService
from web.controllers.api import route_api
from common.models.food.Food import Food
from common.models.member.MemberCart import MemberCart
from common.libs.Helper import selectFilterObj, getDictFilterField


@route_api.route("/cart/index")
def cartIndex():
    resp = {'code': 200, 'msg': 'ok', 'data': {}}
    member_info = g.member_info
    if not member_info:
        resp['code'] = -1
        resp['msg'] = '未登录'
        return jsonify(resp)

    cart_list = MemberCart.query.filter_by(member_id=member_info.id).all()
    data_cart_list = []
    if cart_list:
        food_ids = selectFilterObj(cart_list, 'food_id')
        food_map = getDictFilterField(Food, Food.id, 'id', food_ids)

        for item in cart_list:
            tem_food_info = food_map[item.food_id]
            tmp_data = {
                "id": item.id,
                "food_id": item.food_id,
                "pic_url": UrlManager.buildImageUrl(tem_food_info.main_image),
                "name":tem_food_info.name,
                "price":str( tem_food_info.price ),
                "active": True,
                "number": item.quantity
            }
            data_cart_list.append(tmp_data)
    resp['data']['list'] = data_cart_list

    return jsonify(resp)


@route_api.route("/cart/set", methods=['GET', 'POST'])
def setCart():
    resp = {'code': 200, 'msg': '添加购物车成功~', 'data': {}}
    req = request.values
    food_id = int(req['id']) if 'id' in req else 0
    number = int(req['number']) if 'number' in req else 0
    if food_id < 1 or number < 1:
        resp['code'] = -1
        resp['msg'] = "添加购物车失败-1~~"
        return jsonify(resp)

    member_info = g.member_info
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "添加购物车失败-2~~"
        return jsonify(resp)

    food_info = Food.query.filter_by(id=food_id).first()
    if not food_info:
        resp['code'] = -1
        resp['msg'] = "添加购物车失败-3~~"
        return jsonify(resp)

    if food_info.stock < number:
        resp['code'] = -1
        resp['msg'] = "添加购物车失败,库存不足~~"
        return jsonify(resp)

    ret = CartService.setItems(member_id=member_info.id, food_id=food_info.id, number=number)
    if not ret:
        resp['code'] = -1
        resp['msg'] = "添加购物车失败-4~~"
        return jsonify(resp)
    return jsonify(resp)


@route_api.route("/cart/del", methods=["POST"])
def delCart():
    resp = {'code': 200, 'msg': '删除商品成功~', 'data': {}}
    req = request.values
    params_goods = req.get('goods', None)
    items = []
    if params_goods:
        items = json.loads(params_goods)

    if not items or len(items)<1:
        return jsonify(resp)

    member_info = g.member_info
    if not member_info:
        resp['code'] = -1
        resp['msg'] = '删除购物车失败'
        return jsonify(resp)

    ret = CartService.deleteItem(member_info.id, items)
    if not ret:
        resp['code'] = -1
        resp['msg'] = '删除购物车失败-1'
        return jsonify(resp)
    return jsonify(resp)
















