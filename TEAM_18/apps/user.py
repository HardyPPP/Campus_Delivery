from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash, g
from flask_mail import Mail, Message
from flask import current_app
from decorators import login_required
from exti import mail, db
from models import EmailCaptcha, User, Deliverer, Order, OrderDetail, Shop, Merchants, Commodities
import string, random
from apps.forms import RegisterForm, LoginForm, DLoginForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("user", __name__, url_prefix="/user")

'''

relevant database operation for user/deliverer 

'''


@bp.route("/login", methods=["POST", "GET"])
def login():
    if (not hasattr(g, 'user')) and (not hasattr(g, 'userD')) and (not hasattr(g, 'merchant')):
        # if no user login
        if request.method == "GET":
            # render the login page
            current_app.logger.debug("show user login page")
            return render_template("login.html")
        else:
            current_app.logger.debug("user login request")
            # get the data from form
            form = LoginForm(request.form)
            if form.validate():
                current_app.logger.debug("user login form validate")
                email = form.email.data
                print(email)
                password = form.password.data
                user = User.query.filter_by(email=email).first()
                # compare the password between form data and database
                if user and check_password_hash(user.password_hash, password):
                    # password correct, add current merchant to session
                    session['user_email'] = user.email
                    current_app.logger.debug("user login success")
                    return redirect(url_for("user.index"))
                else:
                    current_app.logger.debug("user login fail, wrong pwd or uid")
                    # password incorrect
                    flash("wrong email or password")
                    return redirect(url_for("user.login"))
            else:
                # data not validate
                current_app.logger.debug("user login form not validate")
                flash("please enter correct email or password")
                return redirect(url_for("user.login", **locals()))
    else:
        current_app.logger.debug("user already login, logout now")
        # if someone already log in, log out first
        return redirect(url_for("user.logout"))


@bp.route("/logout")
def logout():
    session.clear()
    current_app.logger.debug("user logout")
    return render_template("index.html")


@bp.route("/userIndex")
@login_required
def index():
    current_app.logger.debug("user index page")
    return render_template("FrontPageForUser.html", g=g)


@bp.route("/delivererIndex")
@login_required
def indexD():
    current_app.logger.debug("deliverer index page")
    orders = Order.query.filter_by(status=1).all()
    return render_template("OrderRelease.html", g=g, orders=orders)


@bp.route("/userIndexForUnlogin")
def indexForNoLogin():
    current_app.logger.debug("index page for user that has no account ")
    return render_template("index.html")


# user register
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        current_app.logger.debug("show user register page")
        # render the register page
        form = RegisterForm(request.form)
        return render_template("register.html", form=form)
    else:
        current_app.logger.debug("user register request")
        # get the data from form
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.UserName.data
            password = form.password.data
            student_id = form.student_id.data
            phone_number = form.phone_number.data
            location = form.location.data
            password_hash = generate_password_hash(password)
            # creat user object
            user = User(email=email, student_id=student_id, username=username,
                        phone_number=phone_number, password_hash=password_hash,
                        student_address=location)
            db.session.add(user)
            db.session.commit()
            current_app.logger.debug("register data saved successfully")
            # add to database
            return redirect(url_for("user.login"))
        else:
            current_app.logger.debug("user register form not validate")
            if form.UserName.errors:
                flash("username length should between 3 to 12")
            elif form.email.errors:
                flash('incorrect email form or already registered')
            elif form.phone_number.errors:
                flash('incorrect phone number form')
            elif form.student_id.errors:
                flash('incorrect id form')
            elif form.password.errors:
                flash('password length should between 8 and 16')
            elif form.passwordV.errors:
                flash('inconsistent password')

            return redirect(url_for("user.register", form=form))


# email validation
@bp.route("/captcha", methods=["POST"])
def get_captcha():
    current_app.logger.debug("get captcha for a new user")
    # get email
    email = request.form.get("email")
    # generate a 4 digits random varify code
    stri = string.ascii_letters + string.digits
    code = "".join(random.sample(stri, 4))
    # create a message to send
    if email:
        current_app.logger.debug("sending email")
        message = Message(
            subject="test",
            recipients=[email],
            body=f"captcha = {code}",
        )
        print(code)
        mail.send(message)
        current_app.logger.debug("captcha email sent successfully")
        # send email
        captcha_email = EmailCaptcha.query.filter_by(email=email).first()
        if captcha_email:
            # if email exist, update the captcha code
            captcha_email.captcha = code
            captcha_email.create_time = datetime.now()
            current_app.logger.debug("new captcha updated")
            db.session.commit()
        else:
            # if not exist, add the email to database
            captcha_email = EmailCaptcha(email=email, captcha=code)
            db.session.add(captcha_email)
            db.session.commit()
            current_app.logger.debug("new captcha added")
        return jsonify({"code": 200})
    else:
        current_app.logger.debug("not validate email for captcha")
        return jsonify({"code": 400, "message": "please enter correct email"})


@bp.route("/become_deliverer", methods=["GET", "POST"])
@login_required
def become_deliverer():
    if hasattr(g, 'user'):
        # to become a deliverer, you need to first register a user account
        if request.method == 'GET':
            current_app.logger.debug("show deliverer index page")
            # render the page
            return render_template("become_deliverer.html")
        else:
            if g.user:
                d = Deliverer.query.filter_by(email=g.user.email).first()
                if d:
                    current_app.logger.debug("has already become a deliverer")
                    return redirect(url_for("user.deliverer_login"))
                else:
                    current_app.logger.debug("becoming deliverer")
                    # migrate the user data directly to deliverer database
                    deliverer = Deliverer(deliverer_id=g.user.student_id, username=g.user.username, email=g.user.email,
                                          password_hash=g.user.password_hash, phone_number=g.user.phone_number)
                    db.session.add(deliverer)
                    db.session.commit()
                    current_app.logger.debug("becoming deliverer success")
                    return redirect(url_for("user.deliverer_login"))
            else:
                current_app.logger.debug("you need to login as a user to become a deliverer")
                return redirect(url_for("user.login"))
    else:
        current_app.logger.debug("you need to login to become a deliverer")
        return redirect(url_for("user.login"))


@bp.route("/delivererLogin", methods=["GET", "POST"])
def deliverer_login():
    if (not hasattr(g, 'user')) and (not hasattr(g, 'userD')) and (not hasattr(g, 'merchant')):
        # if no user login
        if request.method == 'GET':
            # render the login page
            current_app.logger.debug("show deliverer index page")
            return render_template("deliverer_login.html")
        else:
            current_app.logger.debug("deliverer login request")
            # get the data from form
            form = DLoginForm(request.form)
            if form.validate():
                current_app.logger.debug("deliverer login form validate")
                email = form.email.data
                password = form.password.data
                userD = Deliverer.query.filter_by(email=email).first()
                # compare the password between form data and database
                if userD and check_password_hash(userD.password_hash, password):
                    # password correct, add current merchant to session
                    session['userD_email'] = userD.email
                    current_app.logger.debug("deliverer login success")
                    return redirect(url_for("user.indexD"))
                else:
                    # password incorrect
                    current_app.logger.debug("deliverer login fail, wrong pwd or uid")
                    flash("wrong email or password")
                    return redirect(url_for("user.deliverer_login"))
            else:
                # data not validate
                current_app.logger.debug("deliverer login form not validate")
                flash("please enter correct form of email or password")
                return redirect(url_for("user.deliverer_login"))
    else:
        current_app.logger.debug("deliverer already login ")
        # if someone already log in, log out first
        return redirect(url_for("user.logout"))


@bp.route("/clearDatabase", methods=["GET", "POST"])
def clear_database():
    # delete this detail data
    for de in OrderDetail.query.all():
        db.session.delete(de)
        db.session.commit()
    for o in Order.query.all():
        db.session.delete(o)
        db.session.commit()
    for u in User.query.all():
        db.session.delete(u)
        db.session.commit()
    for m in Merchants.query.all():
        for x in m.shop:
            db.session.delete(x)
            db.session.commit()
        db.session.delete(m)
        db.session.commit()
    for c in Commodities.query.all():
        db.session.delete(c)
        db.session.commit()
    for d in Deliverer.query.all():
        db.session.delete(d)
        db.session.commit()
    for e in EmailCaptcha.query.all():
        db.session.delete(e)
        db.session.commit()
    for s in Shop.query.all():
        db.session.delete(s)
        db.session.commit()
    return redirect(url_for("user.logout"))
