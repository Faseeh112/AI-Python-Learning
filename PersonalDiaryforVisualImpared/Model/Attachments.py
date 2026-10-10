from PersonalDiaryforVisualImpared.db import db
from datetime import datetime

class Attachments(db.Model):
    __tablename__ = 'Attachments'
    Attac_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    File_name = db.Column(db.String(255))
    File_type = db.Column(db.String(50))
    File_path = db.Column(db.String(255))
    Action_type = db.Column(db.String(50))
    context = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

    User_id = db.Column(db.Integer, db.ForeignKey("User.User_id"))
    user_rship = db.relationship('User', back_populates='attachments_rship')