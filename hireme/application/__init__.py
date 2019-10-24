import logging
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import Config

# Generic Flask application factory and required globals

app_directory = os.path.dirname(os.path.realpath(__file__))

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap()
babel = Babel()

def create_app():
    """
    Factory function
    :return: flask application object
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    babel.init_app(app)
    logging.basicConfig(
        filename='logs/hireme-application.log',
        level=logging.DEBUG
    )
    with app.app_context():
        db.create_all()
        return app


def register_blueprints(app):
    """
    Registers the application's blueprints
    (basically different sub-sections of the app.)
    This is useful for organizing the structure
    of larger Flask applications.
    :param app: flask application instance
    :return:
    """
    with app.app_context():
        from application.auth import bp as auth_bp
        from application.errors import bp as errors_bp
        from application.main_app import bp as main_bp
        from application.skills import bp as skills_bp
        app.register_blueprint(errors_bp)
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(skills_bp, url_prefix='/skills')
        app.register_blueprint(main_bp)