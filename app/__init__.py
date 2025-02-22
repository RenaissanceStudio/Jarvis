from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_wtf.csrf import CSRFProtect


from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login.index'
csrf = CSRFProtect()


class Cache:
    pass


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    csrf.init_app(app)

    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)
    #
    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    from .views.main import main_bp
    app.register_blueprint(main_bp)

    from .views.login import login
    app.register_blueprint(login, url_prefix='/login')

    from .views.todo_lists import todo_list
    app.register_blueprint(todo_list, url_prefix='/todo_list')

    from .views.account import register
    app.register_blueprint(register, url_prefix='/register')

    Cache.app = app
    return app


def get_app():
    return Cache.app
