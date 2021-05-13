from flask_login import LoginManager, UserMixin

from app.database import Profile

login_manager = LoginManager()

login_manager.login_view = 'profile.login'
login_manager.login_message = 'Для начала авторизуйтесь'
login_manager.login_message_category = 'warning'


class UserLogin(Profile, UserMixin):
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    return UserLogin.query.get(user_id)