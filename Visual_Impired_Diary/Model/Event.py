from Visual_Impired_Diary.db import db


class Event(db.Model):
	__tablename__ = 'Event'  # Capital E

	Event_id = db.Column(db.Integer, primary_key=True)  # Changed from 'id'
	Name = db.Column(db.String(150))  # Capital N
	Total_event = db.Column(db.Integer)  # Capital T

	detail_rship = db.relationship('DetailEvent', back_populates='event_rship')
	attend_rship = db.relationship('Attend', back_populates='event_rship')