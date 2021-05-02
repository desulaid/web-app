from flask_login import LoginManager, UserMixin

from app.database.models import Profile

login_manager = LoginManager()


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
    return Profile.query.get(user_id)
