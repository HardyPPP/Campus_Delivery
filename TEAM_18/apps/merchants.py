from flask import Blueprint, jsonify, request, render_template, session, redirect, flash, url_for, g
from werkzeug.security import check_password_hash, generate_password_hash

from apps.forms import LoginForm, RegisterForm, MRegisterForm, SRegisterForm, CRegisterForm
from decorators import login_required
from exti import db
from models import User, Merchants, Shop, Commodities
import re

bp = Blueprint("merchant", __name__, url_prefix="/merchant")

'''

relevant database operation for merchant/shop/commodity 

'''


# merchant login
@bp.route("/login", methods=["POST", "GET"])
def login():
    if (not hasattr(g, 'user')) and (not hasattr(g, 'userD')) and (not hasattr(g, 'merchant')):
        # if no user login
        if request.method == "GET":
            form = LoginForm(request.form)
            # render the login page
            return render_template("NewRegForM.html", form=form)
        else:
            # get the data from form
            form = LoginForm(request.form)
            if form.validate():
                email = form.email.data
                password = form.password.data
                merchant = Merchants.query.filter_by(merchants_email=email).first()
                # compare the password between form data and database
                if merchant and check_password_hash(merchant.password_hash, password):
                    # password correct, add current merchant to session
                    session['merchants_email'] = merchant.merchants_email
                    print(session.get('merchants_email'))
                    return redirect(url_for("merchant.index", form=form))
                else:
                    # password incorrect
                    flash("wrong email or password")
                    return redirect(url_for("merchant.login", form=form))
            else:
                # data not validate
                flash("please enter correct form of email or password")
                return redirect(url_for("merchant.login", form=form))
    else:
        # if someone already log in, log out first
        return redirect(url_for("user.logout"))


@bp.route("/merchantIndex")
@login_required
def index():
    return render_template("MainPageForMerchants.html", g=g)


@bp.route("/logout")
def logout():
    # logout and clear session
    session.clear()
    return redirect(url_for("user.indexForNoLogin"))


# merchant register
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        # render the register page
        form = RegisterForm(request.form)
        return render_template("NewRegForM.html", form=form)
    else:
        # get the data from form
        form = MRegisterForm(request.form)
        email = form.email.data
        username = form.UserName.data
        password = form.password.data
        passwordV = form.passwordV.data
        phone_number = form.phone_number.data
        if Merchants.query.filter_by(merchants_email=email).first():
            return jsonify({"code": "sameEmail"})
        elif Merchants.query.filter_by(phone_number=phone_number).first():
            return jsonify({"code": "samePhone"})
        else:
            if form.validate():
                password_hash = generate_password_hash(password)
                # creat merchant object
                merchant = Merchants(merchants_email=email, merchants_name=username,
                                     phone_number=phone_number, password_hash=password_hash)
                # add to database
                db.session.add(merchant)
                db.session.commit()
                # give the merchant a unique shop id
                merchant2 = Merchants.query.filter_by(merchants_email=email).first()
                merchant2.shop_id = merchant2.merchants_id
                print(merchant2.merchants_id)
                db.session.commit()
                return jsonify({"code": "good"})
            else:
                if len(password) > 16 or len(password) < 8:
                    return jsonify({"code": "pwdLength"})
                elif len(username) < 3 or len(username) > 12:
                    return jsonify({"code": "uidLength"})
                elif passwordV != password:
                    return jsonify({"code": "pwdDiffer"})
                elif len(phone_number) != 11:
                    return jsonify({"code": "phoneLength"})
                else:
                    return jsonify({"code": "emailError"})


# register a shop
@bp.route("/registerForShop", methods=["GET", "POST"])
@login_required
# merchant need login first
def register_shop():
    if hasattr(g, 'merchant'):
        if request.method == 'GET':
            form = SRegisterForm(request.form)
            # render the register page
            return render_template("shopAdded.html", form=form)
        else:
            # get the data from form
            form = SRegisterForm(request.form)
            if form.validate():
                shop_name = form.shop_name.data
                shop_location = form.shop_location.data
                merchant = Merchants.query.filter_by(merchants_email=g.merchant.merchants_email)
                # creat shop object
                if merchant.first().shop:
                    flash('you already have a shop')
                    return redirect(url_for("merchant.register_shop", form=form))
                else:
                    shop = Shop(merchant=g.merchant, shop_id=merchant.first().merchants_id, shop_name=shop_name,
                                shop_location=shop_location)
                    # add relationship
                    merchant.shop = shop
                    # add shop to database
                    db.session.add(shop)
                    db.session.commit()
                    return redirect(url_for("merchant.index"))
            else:
                if form.shop_name.errors:
                    flash('shop name length should be at minimum '
                          '3 words or is already registered')
                elif form.shop_location.errors:
                    flash('location length should be at minimum '
                          '3 words')
                return redirect(url_for("merchant.register_shop"))
    else:
        return redirect(url_for("user.logout"))


# register a commodity
@bp.route("/addCommodity", methods=["GET", "POST"])
@login_required
# merchant need login first
def add_commodity():
    if g.merchant.shop:
        if request.method == 'GET':
            # render the register page
            return render_template("addCommodities.html")
        else:
            # get the data from form
            form = CRegisterForm(request.form)
            if form.validate():
                price = form.Price.data
                category = form.Category.data
                name = form.CommodityName.data
                commodity = Commodities(commodity_price=price, commodity_name=name,
                                        category=category, shop_id=g.merchant.shop_id)
                # creat commodity object and add to database
                db.session.add(commodity)
                db.session.commit()
                return redirect(url_for("merchant.add_commodity"))
            else:
                if form.Price.errors:
                    flash('please enter a price')
                elif form.Category.errors:
                    flash('please enter a category')
                elif form.CommodityName.errors:
                    flash('please enter a name')
                return redirect(url_for("merchant.add_commodity"))
    else:
        return redirect(url_for("merchant.register_shop"))
