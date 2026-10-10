from PersonalDiaryforVisualImpared.db import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'User'
    User_id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    DOB = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now)

    query_rship = db.relationship('Query', back_populates='user_rship')
    reminders_rship = db.relationship('Reminders', back_populates='user_rship')
    attachments_rship = db.relationship('Attachments', back_populates='user_rship')
    item_location_rship = db.relationship('Item_location', back_populates='user_rship')
    play_rship = db.relationship('Play', back_populates='user_rship')
    attend_rship = db.relationship('Attend', back_populates='user_rship')