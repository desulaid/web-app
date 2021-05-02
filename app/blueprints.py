from .dashboard import dashboard
from .user import user


def init_blueprints(app: object):
    app.register_blueprint(user)
    app.register_blueprint(dashboard)
