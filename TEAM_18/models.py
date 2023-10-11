from datetime import datetime

from sqlalchemy.orm import backref

from exti import db

from werkzeug.security import generate_password_hash, check_password_hash


# models  in data base
class User(db.Model):
    __tablename__ = 'user'
    student_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone_number = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    student_address = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Deliverer(db.Model):
    __tablename__ = 'deliverer'
    deliverer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone_number = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))


class Merchants(db.Model):
    __tablename__ = 'merchants'
    merchants_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    shop_id = db.Column(db.Integer, autoincrement=True, unique=True)
    phone_number = db.Column(db.String(64), unique=True)
    merchants_name = db.Column(db.String(64), index=True, unique=True)
    merchants_email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))


class Shop(db.Model):
    __tablename__ = 'shop'
    shop_id = db.Column(db.Integer, db.ForeignKey('merchants.shop_id'), primary_key=True)
    shop_name = db.Column(db.String(120))
    shop_location = db.Column(db.String(120))
    merchant = db.relationship("Merchants", backref="shop")


class Commodities(db.Model):
    __tablename__ = "commodities"
    commodity_id = db.Column(db.Integer, primary_key=True)
    commodity_price = db.Column(db.Integer)
    commodity_name = db.Column(db.String(64))
    repository = db.Column(db.Integer)
    category = db.Column(db.String(64))
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.shop_id'))
    shop = db.relationship("Shop", backref="commodities")


class Order(db.Model):
    __tablename__ = "order"
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reciever_id = db.Column(db.Integer, db.ForeignKey('user.student_id'))
    deliverer_id = db.Column(db.Integer, db.ForeignKey('deliverer.deliverer_id'))
    status = db.Column(db.Integer)
    release_time = db.Column(db.DateTime)
    reciever = db.relationship("User", backref="order")
    deliverer = db.relationship("Deliverer", backref="order")


class OrderDetail(db.Model):
    __tablename__ = "orderdetails"
    detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id', ondelete="CASCADE"))
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodities.commodity_id'))
    commodity_number = db.Column(db.Integer)
    order = db.relationship("Order", backref=backref("detail", cascade='all, delete-orphan', passive_deletes=True))
    # 级联删除
    commodity = db.relationship("Commodities", backref="detail")


class EmailCaptcha(db.Model):
    __tablename__ = "emailcaptcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
