from PersonalDiaryforVisualImpared.db import db

class Event(db.Model):
    __tablename__ = 'Event'
    Event_id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Total_event = db.Column(db.String(255))

    attend_rship = db.relationship('Attend', back_populates='event_rship')