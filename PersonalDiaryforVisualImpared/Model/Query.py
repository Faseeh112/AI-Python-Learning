from PersonalDiaryforVisualImpared.db import db
from datetime import datetime


class Query(db.Model):
    __tablename__ = 'Query'
    Query_id = db.Column(db.Integer, primary_key=True)
    Context = db.Column(db.Text)
    Reply = db.Column(db.Text)
    Created_at = db.Column(db.DateTime, default=datetime.now)

    User_id = db.Column(db.Integer, db.ForeignKey("User.User_id"))
    user_rship = db.relationship('User', back_populates='query_rship')