from Visual_Impired_Diary.db import db
from datetime import datetime


class User(db.Model):
	__tablename__ = 'User'  # Table name is 'User' with capital U, not 'user'

	User_id = db.Column(db.Integer, primary_key=True)  # Changed from 'id' to 'User_id'
	Name = db.Column(db.String(100))
	Email = db.Column(db.String(150), unique=True)
	Password = db.Column(db.String(255))
	DOB = db.Column(db.Date)  # Changed from 'dob' to 'DOB' (uppercase)
	created_at = db.Column(db.DateTime, default=datetime.now)

	# Relationships
	reminders_rship = db.relationship('Reminders', back_populates='user_rship', lazy=True)
	attachments_rship = db.relationship('Attachments', back_populates='user_rship', lazy=True)
	item_rship = db.relationship('ItemLocation', back_populates='user_rship', lazy=True)
	attend_rship = db.relationship('Attend', back_populates='user_rship', lazy=True)
