from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def create_app(config_class=Config):
    flask_object = Flask(__name__)
    flask_object.config.from_object(config_class)

    db.init_app(flask_object)
    migrate.init_app(flask_object, db)
    login.init_app(flask_object)

    engine = create_engine(config_class.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind = engine)
    session = Session()

    from app.auth import auth_bp
    flask_object.register_blueprint(auth_bp, url_prefix='/auth')
    from app.tasks import tasks_bp
    flask_object.register_blueprint(tasks_bp, url_prefix='/tasks')

    return flask_object, session

from app import models 
