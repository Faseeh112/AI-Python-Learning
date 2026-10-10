from Visual_Impired_Diary.db import db
from datetime import datetime


class Reminders(db.Model):
	__tablename__ = 'Reminders'  # Capital R

	Reminder_id = db.Column(db.Integer, primary_key=True)  # Changed from 'id'
	Remind_date = db.Column(db.Date)  # Capital R
	Remind_time = db.Column(db.Time)  # Capital R
	Repeat_type = db.Column(db.String(50))  # Capital R
	Remind_content=db.Column(db.String(5000))  # Capital R
	created_at = db.Column(db.DateTime, default=datetime.now)

	User_id = db.Column(db.Integer, db.ForeignKey("User.User_id"))  # Changed to match User table
	user_rship = db.relationship('User', back_populates='reminders_rship')

	play_rship = db.relationship('Play', back_populates='reminder_rship', lazy=True)