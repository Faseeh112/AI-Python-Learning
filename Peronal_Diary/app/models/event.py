"""
Event — user events linked to host person and location.
"""
from app.extensions import db
from datetime import datetime


class Event(db.Model):
    __tablename__ = 'event'

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    host_person_id = db.Column(db.Integer,
                               db.ForeignKey('person.person_id', ondelete='NO ACTION'),
                               nullable=True)
    location_id = db.Column(db.Integer,
                            db.ForeignKey('location.location_id', ondelete='NO ACTION'),
                            nullable=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=True)
    event_type = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(2000), nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # ── One-to-Many ────────────────────────────────────────────
    reminders = db.relationship('Reminder', backref='event', lazy='dynamic')
    transactions = db.relationship('TransactionLog', backref='event', lazy='dynamic')

    def __repr__(self):
        return f'<Event {self.event_id}: {self.title}>'
