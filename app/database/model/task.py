from app.database.sqlalchemy import db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=True)
    datetime = db.Column(db.DateTime, nullable=False)
    student = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    attended = db.Column(db.Boolean, nullable=False)
    comment = db.Column(db.String(256), nullable=True)

    def __init__(self, title: str, attended: bool, comment: str, datetime: datetime, student_id: int) -> object:
        self.title = title
        self.attended = attended
        self.comment = comment
        self.datetime = datetime
        self.student = student_id
