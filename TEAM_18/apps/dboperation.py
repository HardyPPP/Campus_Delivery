from flask import Blueprint

from app import db
from models import User, Deliverer, Merchants, Shop, Commodities, Order, OrderDetail

bp = Blueprint("dboperation", __name__, url_prefix="/dbop")

'''

this file is just for database operation test, not used in the project

'''


@bp.route("/addUser")
def add_user():
    user = User(student_id=20372215, username='hardy', email='3374618571@qq.com', phone_number='18722396825',
                password_hash='hardy2001', student_address='Building 11')
    db.session.add(user)
    db.session.commit()
    print(user.username)
    return "ds"


@bp.route("/addDeliverer")
def add_deliverer():
    deliverer = Deliverer(deliverer_id=20372215, username='harDy', email='3374618571@qq.com',
                          phone_number='18722396825', password_hash='hardy2001')
    db.session.add(deliverer)
    db.session.commit()
    print(deliverer.username)
    return "ds"


@bp.route("/addShop")
def add_shop():
    merchant = Merchants.query.filter_by(merchants_id=1)
    shop = Shop(shop_id=1, shop_name="强子烤冷面", shop_location='美食园二楼')
    merchant.shop = shop
    db.session.add(shop)
    db.session.commit()
    print(merchant.shop.shop_name)
    print(shop.merchant.merchants_name)
    return "ds"


@bp.route("/addMerchant")
def add_merchant():
    merchant = Merchants(shop_id=1, phone_number="12091029", merchants_name="强子", merchants_email='137742666@qq.com')
    db.session.add(merchant)
    db.session.commit()
    print(merchant.merchants_email)

    return "df"


@bp.route("/addCommodity")
def add_commodity():
    shop = Shop.query.filter_by(shop_id=1)
    commodity = Commodities(commodity_price=7, commodity_name='招牌烤冷面', repository=10, category="小吃",
                            shop_id=shop[0].shop_id)
    shop.commodities = commodity
    db.session.add(commodity)
    db.session.commit()
    print(shop[0].shop_name)
    print(shop.commodities.commodity_name)
    return "ds"


@bp.route("/addOrder")
def add_order():
    user = User.query.filter_by(student_id="20372215")[0]
    deliverer = Deliverer.query.filter_by(deliverer_id='20372215')[0]
    order = Order(reciever_id=user.student_id, deliverer_id=deliverer.deliverer_id, status=0)
    db.session.add(order)
    db.session.commit()
    return 'ss'


@bp.route("/addOrderDetail")
def add_order_detail():
    order = Order.query.filter_by(order_id=1)
    order_detail = OrderDetail(commodity_id=9, order_id=order[0].order_id, commodity_number=1)
    order.detail = order_detail
    db.session.add(order_detail)
    db.session.commit()
    return "ss"


@bp.route("/deleteUser")
def delete_user():
    User.query.filter_by(student_id=20372215).delete()
    db.session.commit()
    return "11"


@bp.route("/deleteOrder")
def delete_order():
    order = Order.query.filter_by(order_id=1)
    order.delete()
    db.session.commit()
    return "11"
