import wtforms
from wtforms.validators import length, email, EqualTo, InputRequired
from models import EmailCaptcha, User, Merchants, Shop

'''

forms used for data validation 

'''


# user login form validation
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=8, max=16)])


# user register form validation
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[email(message='incorrect email form')])
    password = wtforms.StringField(
        validators=[length(min=8, max=16, message='password length should between 8 and 16')])
    passwordV = wtforms.StringField(validators=[EqualTo("password", message='inconsistent password')])
    UserName = wtforms.StringField(validators=[length(min=3, max=12, message='username length should between 3 to 12')])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    student_id = wtforms.StringField(validators=[length(min=8, max=8)])
    phone_number = wtforms.StringField(validators=[length(min=11, max=11, message='incorrect phone number form')])
    location = wtforms.StringField(validators=[length(min=0, max=100)])

    # validation for captcha
    def validate_captcha(self, field):
        captcha = field.data
        email2 = self.email.data
        captcha_model = EmailCaptcha.query.filter_by(email=email2).first()
        if not (captcha_model and captcha_model.captcha.lower() == captcha.lower()):
            raise wtforms.ValidationError("wrong captcha")

    # validation for duplicated email registered
    def validate_email(self, field):
        email = field.data
        if User.query.filter_by(email=email).first():
            raise wtforms.ValidationError("already registered")


# merchant register form validation
class MRegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[email(message='incorrect email form')])
    password = wtforms.StringField(
        validators=[length(min=8, max=16, message='password length should between 8 and 16')])
    passwordV = wtforms.StringField(validators=[EqualTo("password", message='inconsistent password')])
    UserName = wtforms.StringField(validators=[length(min=3, max=12, message='username length should between 3 to 12')])
    phone_number = wtforms.StringField(validators=[length(min=11, max=11, message='incorrect phone number form')])
    def validate_email(self, field):
        email = field.data
        if Merchants.query.filter_by(merchants_email=email).first():
            raise wtforms.ValidationError("already registered")


# shop register form validation
class SRegisterForm(wtforms.Form):
    shop_name = wtforms.StringField(validators=[length(min=3, max=50, message='shop name length should be at minimum '
                                                                              '3 words')])
    shop_location = wtforms.StringField(
        validators=[length(min=3, max=50, message='shop name length should be at minimum '
                                                  '3 words')])

    #  validation for duplicated shop name
    def validate_shop(self, field):
        shop_name = field.data
        if Shop.query.filter_by(shop_name=shop_name).first():
            raise wtforms.ValidationError("already registered")


# deliverer login form validation
class DLoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email(message='incorrect email form')])
    password = wtforms.StringField(
        validators=[length(min=8, max=16, message='password length should between 8 and 16')])


# commodity register form validation
class CRegisterForm(wtforms.Form):
    CommodityName = wtforms.StringField(
        validators=[length(min=1, max=50, message='commodity name length should be at minimum '
                                                  '3 words')])
    Price = wtforms.IntegerField(validators=[InputRequired()])
    Category = wtforms.StringField(validators=[length(min=1, max=50)])


# form validation for passing specific shop id
class ShopForm(wtforms.Form):
    shop_id = wtforms.IntegerField(validators=[InputRequired()])


# form validation for passing specific commodity id
class OrderItemForm(wtforms.Form):
    commodity_id = wtforms.IntegerField(validators=[InputRequired()])


# form validation for passing specific order id
class OrderDetailForm(wtforms.Form):
    order_id = wtforms.StringField(validators=[InputRequired()])


# form validation for passing specific order id
class OrderDetailForm2(wtforms.Form):
    order_id2 = wtforms.StringField(validators=[InputRequired()])


class OrderDetailForm11(wtforms.Form):
    order_id11 = wtforms.StringField(validators=[InputRequired()])



# form validation for passing specific order detail id
class DetailForm(wtforms.Form):
    detail_id = wtforms.StringField(validators=[InputRequired()])