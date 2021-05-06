from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

from .sqlalchemy import db


# Профили старост
class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(256), nullable=False, unique=True)
    _password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=True)
    verify = db.Column(db.Boolean, nullable=False)

    # Группа
    group_id = db.Column(db.Integer, db.ForeignKey(
        "groups.id"), nullable=True)
    group = db.relationship("Group", foreign_keys=[group_id])

    # Преподаватель
    teacher_id = db.Column(db.Integer, db.ForeignKey(
        "teachers.id"), nullable=True)
    teacher = db.relationship("Teacher", foreign_keys=[teacher_id])

    def __init__(self, login, password, name, verify, group_id=None, teacher_id=None):
        self.login = login
        self.password = password
        self.name = name
        self.verify = verify
        self.group_id = group_id
        self.teacher_id = teacher_id

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self.password, value)


# Обычные студенты группы
class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)

    master_id = db.Column(db.Integer, db.ForeignKey(
        "profiles.id"), nullable=True)
    master = db.relationship("Profile", foreign_keys=[master_id])

    def __init__(self, name, master_id=None):
        self.name = name
        self.master_id = master_id


# Преподаватели (классный руководитель)
class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)

    def __init__(self, name):
        self.name = name


# Группы
class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)

    def __init__(self, name, teacher_id=None):
        self.name = name


# Записи
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=True)
    datetime = db.Column(db.DateTime, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey(
        "profiles.id"), nullable=False)
    author = db.relationship("Profile", foreign_keys=[author_id])

    def __init__(self, name, datetime, author_id):
        self.name = name
        self.datetime = datetime
        self.author_id = author_id

class Archive(db.Model):
    __tablename__ = 'archive'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(256), nullable=True)
    attended = db.Column(db.Boolean, nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey(
        "posts.id"), nullable=False)
    post = db.relationship("Post", foreign_keys=[post_id])

    student_id = db.Column(db.Integer, db.ForeignKey(
        "students.id"), nullable=True)
    student = db.relationship("Student", foreign_keys=[student_id])

    def __init__(self, comment, attended, student_id, post_id):
        self.comment = comment
        self.attended = attended
        self.student_id = student_id
        self.post_id = post_id
