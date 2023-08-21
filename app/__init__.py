from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS

db = SQLAlchemy()
app = Flask(__name__)
mail = Mail()

def create_app():
    app.config.from_object('config.Config')
    db.init_app(app)
    mail.init_app(app)
    CORS(app)
    from . import views
    return app