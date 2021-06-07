from app.database.sqlalchemy import db


class Post (db.Model):
    __tablename__ = 'posts'

    id = db.Column (db.Integer, primary_key=True)
    profile = db.Column (db.Integer, db.ForeignKey ('profiles.id'))
    tasks = db.relationship ('Task', secondary='tasks_posts', backref='post', lazy='dynamic')


tasks_posts = db.Table ('tasks_posts',
                        db.Column ('task_id', db.Integer, db.ForeignKey ('tasks.id')),
                        db.Column ('post_id', db.Integer, db.ForeignKey ('posts.id'))
                        )
