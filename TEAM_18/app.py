from flask import Flask, session, g
from flask_migrate import Migrate
from exti import db, mail, logger
from apps import order_bp, user_bp, dboperation_bp, merchant_bp, sd_bp
from models import User, Merchants, Deliverer

app = Flask(__name__)
# config
app.config.from_pyfile("config.txt")
logger.init_app(app)
# initialize database
db.init_app(app)
# initialize mail
mail.init_app(app)
# blueprint register
app.register_blueprint(order_bp)
app.register_blueprint(user_bp)
app.register_blueprint(dboperation_bp)
app.register_blueprint(merchant_bp)
app.register_blueprint(sd_bp)
# database migration
migrate = Migrate(app, db)


@app.before_request
# identify if someone has log in and their identity
def before_request():
    user_email = session.get('user_email')
    merchant_email = session.get('merchants_email')
    userD_email = session.get('userD_email')
    if user_email:
        # a user login
        try:
            user = User.query.filter_by(email=user_email).first()
            # set global variable "user"
            # setattr(g, "user", user)
            g.user = user
        except:
            g.user = None
    if merchant_email:
        # a merchant login
        try:
            merchant = Merchants.query.filter_by(merchants_email=merchant_email).first()
            # set global variable "merchant"
            setattr(g, "merchant", merchant)
            #g.merchant = merchant
        except:
            setattr(g, "merchant", None)
    if userD_email:
        # a deliverer login
        try:
            userD = Deliverer.query.filter_by(email=userD_email).first()
            # set global variable "userD" (deliverer)
            setattr(g, "userD", userD)
        except:
            setattr(g, "userD", None)


@app.context_processor
def context_processor():
    # return current global variable
    if hasattr(g, "user"):
        return {'user': g.user}
    elif hasattr(g, 'merchant'):
        return {'merchant': g.merchant}
    elif hasattr(g, 'userD'):
        return {'userD': g.userD}
    else:
        return {}


if __name__ == '__main__':
    app.run()
