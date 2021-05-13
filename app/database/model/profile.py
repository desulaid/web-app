from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

from app.database.sqlalchemy import db


class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(256), nullable=False, unique=True)
    _password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=True)
    verify = db.Column(db.Boolean, nullable=False)
    role = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)
    group = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=True)
    teacher = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=True)

    def __init__(self, login: str, password: str, name: str, verify: bool, role_id: int = None, group_id: int = None, teacher_id: int = None):
        self.login = login
        self.password = password
        self.name = name
        self.verify = verify
        self.group = group_id
        self.teacher = teacher_id
        self.role = role_id

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self.password, value)
