from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

def create_app():
    app.config.from_object('config.Config')
    db.init_app(app)
    from . import views
    return app