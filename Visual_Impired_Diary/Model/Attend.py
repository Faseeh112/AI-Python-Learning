from Visual_Impired_Diary.db import db


class Attend(db.Model):
	__tablename__ = 'Attend'  # Capital A

	Attend_id = db.Column(db.Integer, primary_key=True)  # Changed from 'id'

	User_id = db.Column(db.Integer, db.ForeignKey("User.User_id"))
	Event_id = db.Column(db.Integer, db.ForeignKey("Event.Event_id"))

	user_rship = db.relationship('User', back_populates='attend_rship')
	event_rship = db.relationship('Event', back_populates='attend_rship')