from app.database.sqlalchemy import db


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    profile = db.Column (db.Integer, db.ForeignKey ("profiles.id"), nullable=True)

    def __init__(self, name: str, profile: int):
        self.name = name
        self.profile = profile
