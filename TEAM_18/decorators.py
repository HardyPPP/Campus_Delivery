from flask import g, redirect,url_for
from functools import  wraps


def login_required(func):
    # identify if a user/merchant/deliverer login
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g,'user'):
            return func(*args, **kwargs)
        elif hasattr(g, 'merchant'):
            return func(*args, **kwargs)
        elif hasattr(g, 'userD'):
            return func(*args, **kwargs)
        else:
            # if no one login, redirect to login page
            return redirect(url_for("user.login"))
    return wrapper