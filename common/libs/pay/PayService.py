import decimal, time
import hashlib
import random

from application import db
from common.libs.Helper import getCurrentData
from common.libs.food.FoodService import FoodService
from common.models.food.Food import Food
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem
from common.models.pay.PayOrderCallbackData import PayOrderCallbackDatum



class PayService():
    def __init__(self):
        pass

    def createOrder(self, member_id, items=None, params=None):
        resp = {"code": 200, "msg": "操作成功", "data": {}}
        pay_price = decimal.Decimal(0.00)
        continue_cnt = 0
        foods_id = []
        for item in items:
            if decimal.Decimal(item['price'])<0:
                continue_cnt += 1
                continue
            pay_price = pay_price + decimal.Decimal(item['price']) * int(item['number'])
            foods_id.append(item['id'])

        if continue_cnt >= len(items):
            resp['code'] = -1
            resp['msg'] = '商品items为空'
            return  resp
        yun_price = params.get('yun_price', 0)
        note = params.get('note', '')
        yun_price = decimal.Decimal(yun_price)
        total_price = pay_price + yun_price
        try:
            # 锁
            tmp_food_list = db.session.query(Food).filter(Food.id.in_(foods_id)).with_for_update().all()
            # 创建列表得到{food.id: 库存}
            tmp_food_stock_mapping = {}
            for tmp_item in tmp_food_list:
                tmp_food_stock_mapping[tmp_item.id] = tmp_item.stock

            model_pay_order = PayOrder()
            model_pay_order.order_sn = self.geneOrderSn()
            model_pay_order.member_id = member_id
            model_pay_order.total_price = total_price
            model_pay_order.yun_price = yun_price
            model_pay_order.pay_price = pay_price
            model_pay_order.note = note
            model_pay_order.status = -8
            model_pay_order.express_status = -8
            # model_pay_order.express_address_id = express_address_id
            # model_pay_order.express_info = json.dumps(express_info)
            model_pay_order.updated_time = model_pay_order.created_time = getCurrentData()
            db.session.add(model_pay_order)
            # db.session.flush()
            for item in items:
                tmp_left_stock = tmp_food_stock_mapping[item['id']]

                if decimal.Decimal(item['price']) < 0:
                    continue
                # 库存不够
                if int(item['number']) > int(tmp_left_stock):
                    raise Exception("您购买的这美食太火爆了，剩余：%s,你购买%s~~" % (tmp_left_stock, item['number']))

                # 库存减少
                tmp_ret = Food.query.filter_by(id=item['id']).update({
                    "stock": int(tmp_left_stock) - int(item['number'])
                })
                if not tmp_ret:
                    raise Exception("下单失败请重新下单")

                tmp_pay_item = PayOrderItem()
                tmp_pay_item.pay_order_id = model_pay_order.id
                tmp_pay_item.member_id = member_id
                tmp_pay_item.quantity = item['number']
                tmp_pay_item.price = item['price']
                tmp_pay_item.food_id = item['id']
                tmp_pay_item.note = note
                tmp_pay_item.updated_time = tmp_pay_item.created_time = getCurrentData()
                db.session.add(tmp_pay_item)
                # db.session.flush()
                # 修改库存
                FoodService.setStockChangeLog(item['id'], -item['number'], "在线购买")
            db.session.commit()
            resp['data'] = {
                'id': model_pay_order.id,
                'order_sn': model_pay_order.order_sn,
                'total_price': str(total_price)
            }
        except Exception as e:
            db.session.rollback()
            print(e)
            resp['code'] = -1
            resp['msg'] = "下单失败请重新下单"
            resp['msg'] = str(e)
            return resp
        return resp

    def geneOrderSn(self):
        m = hashlib.md5()
        sn = None
        while True:
            str = "%s-%s" % (int(round(time.time() * 1000)), random.randint(0, 9999999))
            m.update(str.encode("utf-8"))
            sn = m.hexdigest()
            if not PayOrder.query.filter_by(order_sn=sn).first():
                break
        return sn