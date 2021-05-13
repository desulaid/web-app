
from flask import Flask
from .database import db
from .cli import cli
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

    app.register_blueprint(profile)
    app.register_blueprint(dashboard)
