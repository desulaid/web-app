__author__ = 'desulaid'
__version__ = '0.0.2'
__email__ = 'desulaid@gmail.com'

from flask import Flask

from .cli import cli
from .database import db
from .profile import login_manager


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('app.config')
    app.cli.add_command(cli)
    db.init_app(app)
    login_manager.init_app(app)
    register_blueprints(app)

    return app


def register_blueprints(app: Flask) -> None:
    from .profile import profile
    from .dashboard import dashboard
    from .home import home

    app.register_blueprint(profile)
    app.register_blueprint(dashboard)
    app.register_blueprint(home)
