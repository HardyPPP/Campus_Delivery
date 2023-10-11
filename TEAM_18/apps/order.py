from flask import Blueprint, render_template, g, request, jsonify, redirect, url_for
from decorators import login_required
from apps.forms import OrderItemForm, OrderDetailForm,OrderDetailForm2,DetailForm,OrderDetailForm11
from models import Order, OrderDetail, User
from exti import db
import datetime
from time import strftime
bp = Blueprint("order", __name__, url_prefix="/")

'''

relevant database operation for Order/OrderDetail 

'''


@bp.route("/")
def index():
    # main index page of the project
    return render_template("index.html")

@bp.route("/11")
def index33():
    # main index page of the project
    return render_template("Base_for_Rider.html")


@bp.route("/order/addNewOrder", methods=["POST"])
@login_required
def add_order():
    # main index page of the project
    if hasattr(g, 'user'):
        # only user could make order
        form = OrderItemForm(request.form)
        if form.validate():
            # if the commodity id is found
            commodity_id = form.commodity_id.data
            user = User.query.filter_by(email=g.user.email).first()
            # get the user
            order = Order.query.filter_by(reciever_id=user.student_id, status=0).first()
            # get this user's unfinished order (if any)
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            #get date
            if order is None:
                # if the user does not have an unfinished order, then create a new one
                new_order = Order(reciever_id=user.student_id, status=0, release_time = datetime.datetime.now())
                print(user.student_id)
                db.session.add(new_order)
                db.session.commit()
                # after creation, add this chosen commodity to the order
                order2 = Order.query.filter_by(reciever_id=user.student_id, status=0).first()
                order_detail = OrderDetail(order_id=order2.order_id, commodity_id=commodity_id, commodity_number=1)
                db.session.add(order_detail)
                db.session.commit()
            else:
                # the user has an unfinished order, directly add the commodity to it
                order_detail = OrderDetail(order_id=order.order_id, commodity_id=commodity_id, commodity_number=1)
                db.session.add(order_detail)
                db.session.commit()
            return jsonify({"code": 200})
        else:
            return jsonify({"code": 400, "message": "check internet connection"})



@bp.route("/order/myOrder", methods=["POST", "GET"])
@login_required
def show_my_order():
    # show all the orders of this user
    if hasattr(g, 'user'):
        # find the current user by email
        user = User.query.filter_by(email=g.user.email).first()
        # find the user's all orders
        orders = Order.query.filter_by(reciever_id=user.student_id).all()
        return render_template("ShoppingCart.html", orders=orders)
    else:
        return redirect(url_for("user.login"))


@bp.route("/order/viewDetail", methods=["POST", "GET"])
@login_required
def view_my_detail():
    # show the order detail of this order
    form = OrderDetailForm(request.form)
    if form.validate():
        # if the order id is found
        order_id = form.order_id.data
        # find the order by its id, and pass this data to html
        orders = Order.query.filter_by(order_id=order_id).first()
        return render_template("oreder.html", order=orders)
    else:
        return jsonify({"code": 400, "message": "check internet connection"})


@bp.route("/order/submit", methods=["POST", "GET"])
@login_required
def submit():
    # submit and finish the order
    if hasattr(g, 'user'):
        # only user can do this
        form = OrderDetailForm2(request.form)
        if form.validate():
            # if the order id is found
            order_id = form.order_id2.data
            order = Order.query.filter_by(order_id=order_id).first()
            # update its current status to 1
            # status numbers:
            # 0 --- unfinished order, waiting for adding new commodity
            # 1 --- finished order, waiting for taken by deliverers
            # 2 --- order that has been taken by a deliverer, but not yet received by user
            # 3 --- completed order, the user has received it
            order.status=1
            db.session.commit()
            return jsonify({"code": 200})
        else:
            print("Novalidate")
            return jsonify({"code": 400, "message": "check internet connection"})
    else:
        print("NotUser")
        return jsonify({"code": 400, "message": "check internet connection"})


@bp.route("/order/delete", methods=["POST", "GET"])
@login_required
def delete():
    # delete an unfinished order
    if hasattr(g, 'user'):
        form = OrderDetailForm(request.form)
        if form.validate():
            # if the order id is found
            order_id = form.order_id.data
            order = Order.query.filter_by(order_id=order_id).first()
            db.session.query(OrderDetail).filter_by(order_id=order_id).delete()
            # delete both the order and its content
            db.session.delete(order)
            db.session.commit()
            return jsonify({"code": 200})
        else:
            print("Novalidate2")
            return jsonify({"code": 400, "message": "check internet connection"})
    else:
        print("NotUser")
        return jsonify({"code": 400, "message": "check internet connection"})


@bp.route("/order/deleteDetail", methods=["POST", "GET"])
@login_required
def delete_detail():
    # delete some content of the order
    if hasattr(g, 'user'):
        # only user can do this
        form = DetailForm(request.form)
        if form.validate():
            # if the order detail id is found
            detail_id = form.detail_id.data
            detail = OrderDetail.query.filter_by(detail_id=detail_id).first()
            # delete this detail data
            db.session.delete(detail)
            db.session.commit()
            return jsonify({"code": 200})
        else:
            print("Novalidate2")
            return jsonify({"code": 400, "message": "check internet connection"})
    else:
        print("NotUser")
        return jsonify({"code": 400, "message": "check internet connection"})


@bp.route("/order/allOrder", methods=["POST", "GET"])
@login_required
def all_order():
    # show all the finished order that waiting for taken by deliverers
    if hasattr(g, 'userD'):
        # only deliverer can see this
        orders =  Order.query.filter_by(status=1).all()
        # find all the status-1 orders and pass them to html
        return render_template("OrderRelease.html",g=g, orders=orders)
    else:
        return jsonify({"code": 400, "message": "check internet connection"})



@bp.route("/order/viewDetail1", methods=["POST", "GET"])
@login_required
def view_1_detail():
    # show the order detail of this order
    form = OrderDetailForm(request.form)
    if form.validate():
        # if the order id is found
        order_id = form.order_id.data
        # find the order by its id, and pass this data to html
        orders = Order.query.filter_by(order_id=order_id).first()
        return render_template("OrderDetailForRider.html", order=orders)
    else:
        return jsonify({"code": 400, "message": "check internet connection"})



@bp.route("/order/accept", methods=["POST", "GET"])
@login_required
def accept():
    # take the order
    if hasattr(g, 'userD'):
        # only deliverer can do this
        form = OrderDetailForm(request.form)
        if form.validate():
            # if the order id is found
            order_id = form.order_id.data
            order = Order.query.filter_by(order_id=order_id).first()
            # update its current status to 1
            # status numbers:
            # 0 --- unfinished order, waiting for adding new commodity
            # 1 --- finished order, waiting for taken by deliverers
            # 2 --- order that has been taken by a deliverer, but not yet received by user
            # 3 --- completed order, the user has received it
            order.status=2
            order.deliverer_id=g.userD.deliverer_id
            db.session.commit()
            return redirect(url_for("user.indexD"))
        else:
            print("Novalidate")
            return jsonify({"code": 400, "message": "check internet connection"})
    else:
        print("NotUser")
        return jsonify({"code": 400, "message": "check internet connection"})



@bp.route("/order/myAcceptOrder", methods=["POST", "GET"])
@login_required
def all_myD_order():
    # show all the accepted order of this deliverers
    if hasattr(g, 'userD'):
        # only deliverer can see this
        orders =  Order.query.filter_by(deliverer_id=g.userD.deliverer_id).all()
        # find all the status-1 orders and pass them to html
        return render_template("MyOrders_D.html", order=orders)
    else:
        return jsonify({"code": 400, "message": "check internet connection"})


@bp.route("/order/confirm", methods=["POST", "GET"])
@login_required
def confirm():
    # confirm deliver
    if hasattr(g, 'user'):
        # only user can do this
        form = OrderDetailForm(request.form)
        if form.validate():
            # if the order id is found
            order_id = form.order_id.data
            order =  Order.query.filter_by(order_id=order_id).first()
            order.status = 3
            db.session.commit()
            return jsonify({"code": 200})
        else:
            return jsonify({"code": 400, "message": "check internet connection"})
    else:
        print("notuser")
        return jsonify({"code": 400, "message": "check internet connection"})