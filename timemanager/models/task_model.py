from flask_login import UserMixin

from timemanager import db


class Task(db.Model, UserMixin):
    """Task model class"""
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    minutes = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    comments = db.Column(db.String, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
