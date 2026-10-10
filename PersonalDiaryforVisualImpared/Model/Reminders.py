from PersonalDiaryforVisualImpared.db import db
from datetime import datetime

# class Reminders(db.Model):
#     __tablename__ = 'Reminders'
#     Reminder_id = db.Column(db.Integer, primary_key=True)
#     Remind_date = db.Column(db.Date)
#     Remind_time = db.Column(db.Time)
#     Repeat_type = db.Column(db.String(50))
#     created_at = db.Column(db.DateTime, default=datetime.now)
#
#     User_id = db.Column(db.Integer, db.ForeignKey("User.User_id"))
#     user_rship = db.relationship('User', back_populates='reminders_rship')

class Reminders(db.Model):
    __tablename__ = 'Reminders'
    Reminder_id = db.Column(db.Integer, primary_key=True)
    Remind_date = db.Column(db.Date)
    Remind_time = db.Column(db.Time)
    Repeat_type = db.Column(db.String(50))
    remind_content = db.Column(db.String(500)) # <--- Add this line
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    User_id = db.Column(db.Integer, db.ForeignKey('User.User_id'))
    user_rship = db.relationship('User', back_populates='reminders_rship')