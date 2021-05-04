import click
from click import command
from flask import Flask, current_app
from flask.cli import with_appcontext

from .database import db
from .profile import login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')
    db.init_app(app)
    login_manager.init_app(app)
    app.cli.add_command(database)

    from .dashboard import dashboard
    from .profile import profile

    app.register_blueprint(dashboard)
    app.register_blueprint(profile)

    return app


def slobkoll_data():
    from .database import Teacher, Group

    groups = current_app.config['COLLEGE_GROUPS']
    teachers = current_app.config['COLLEGE_TEACHERS']

    for item in groups:
        db.session.add(Group(name=item))

    for item in teachers:
        db.session.add(Teacher(name=item))

    db.session.commit()


def create_admin():
    from .database import Profile

    data = current_app.config['ADMIN_PROFILE']
    login = data['login']
    password = data['password']
    name = data['name']
    admin = Profile(name=name,
                    login=login,
                    password=password,
                    verify=True)
    db.session.add(admin)
    db.session.commit()

    return login, password


@command('database')
@with_appcontext
def database():
    """Создать базу данных"""
    db.drop_all()
    db.create_all()
    login, password = create_admin()
    click.echo(f'Данные от админисратора: {login}: {password}')
    slobkoll_data()
