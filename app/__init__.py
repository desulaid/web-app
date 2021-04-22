from click import command
from flask import Flask
from flask.cli import with_appcontext
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(settings):
    app = Flask(__name__)
    app.config.from_object(f'app.settings.{settings}')

    db.init_app(app)
    app.cli.add_command(migrate_db)
    login_manager.init_app(app)

    login_manager.login_view = 'account.login'
    login_manager.login_message = 'Пожалуйста, авторизуйтесь'
    login_manager.login_message_category = 'warning'

    from .account import account
    from .dashboard import dashboard

    app.register_blueprint(account)
    app.register_blueprint(dashboard)

    return app

def account_status_db():
    from .models import Status

    statuses = [
        'Пользователь',
        'Администратор'
    ]

    for i in statuses:
        db.session.add(Status(name=i))

    db.session.commit()

@command('migrate')
@with_appcontext
def migrate_db():
    """Create a database"""
    db.drop_all()
    db.create_all()
    account_status_db()
