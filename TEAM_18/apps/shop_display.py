from flask import Blueprint, request, render_template, session, redirect, flash, url_for, g
from werkzeug.security import check_password_hash, generate_password_hash

from apps.forms import LoginForm, RegisterForm, MRegisterForm, SRegisterForm, CRegisterForm, ShopForm
from decorators import login_required
from exti import db
from models import User, Merchants, Shop, Commodities
from app import db
from models import User, Deliverer, Merchants, Shop, Commodities, Order, OrderDetail

bp = Blueprint("shop_display", __name__, url_prefix="/shopList")


@bp.route("/shops", methods=["GET", "POST"])
def display_all():
    # display all shops in database
    shops = Shop.query.order_by(db.text("shop_name")).all()
    return render_template("ShoopingList.html", shops=shops)


@bp.route("/commodityList", methods=["GET", "POST"])
def display_commodities():
    # display all commodities in oe shop
    form = ShopForm(request.form)
    # get the shop name and search its commodities
    if form.validate():
        shop_id = form.shop_id.data
        shop = Shop.query.filter_by(shop_id=shop_id).first()
        print("you've entered: ")
        print(shop_id)
        if hasattr(g, 'user'):
            return render_template("ShopItem.html", shop=shop,g=g)
        elif hasattr(g, 'merchant'):
            return render_template("ShopItemD.html",shop=shop,g=g)
        else:
            return render_template("ShopItem.html", shop=shop, g=g)
    else:
        return redirect(url_for("shop_display.display_all"))




@bp.route("/login")
def LoginFirst():
    return render_template("login.html")
