from Visual_Impired_Diary.db import db
from datetime import datetime


class Attachments(db.Model):
	__tablename__ = 'Attachments'  # Capital A

	Attac_id = db.Column(db.Integer, primary_key=True)  # Changed from 'id'
	File_name = db.Column(db.String(255))  # Capital F
	File_type = db.Column(db.String(50))  # Capital F
	File_path = db.Column(db.String(255))  # Capital F
	Action_type = db.Column(db.String(50))  # Capital A
	context = db.Column(db.String(255))  # lowercase
	created_at = db.Column(db.DateTime, default=datetime.now)

	User_id = db.Column(db.Integer, db.ForeignKey("User.User_id"))
	user_rship = db.relationship('User', back_populates='attachments_rship')
