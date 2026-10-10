from Visual_Impired_Diary.db import db
from datetime import datetime


class DetailEvent(db.Model):
	__tablename__ = 'Detail_event'  # lowercase 'e' in event

	Detail_id = db.Column(db.Integer, primary_key=True)  # Changed from 'id'
	Event_id = db.Column(db.Integer, db.ForeignKey("Event.Event_id"))
	Title = db.Column(db.String(150))  # Capital T
	Context = db.Column(db.String(255))  # Capital C
	Date = db.Column(db.Date)  # Capital D
	_Transaction = db.Column(db.String(150))  # Capital T
	Transaction_Type = db.Column(db.String(100))  # Capital T
	created_at = db.Column(db.DateTime, default=datetime.now)

	event_rship = db.relationship('Event', back_populates='detail_rship')