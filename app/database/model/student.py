from app.database.sqlalchemy import db


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    profile = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False)

    def __init__(self, name: str, profile_id: int):
        self.name = name
        self.profile = profile_id
