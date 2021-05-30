from app.database.sqlalchemy import db


class Role (db.Model):
    __tablename__ = 'roles'

    id = db.Column (db.Integer, primary_key=True)
    name = db.Column (db.String (256), nullable=False)

    def __init__ (self, name: str):
        self.name = name
