from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from log import Logger

logger = Logger()

# avoid duplicate call
db = SQLAlchemy()
mail = Mail()
