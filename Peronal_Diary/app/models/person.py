"""
Person — contacts and relations for a user.
Linked to transactions, events, and notes.
"""
from app.extensions import db
from datetime import datetime


class Person(db.Model):
    __tablename__ = 'person'

    person_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    name = db.Column(db.String(100), nullable=False)
    relation = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    notes = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # ── Constraints ────────────────────────────────────────────
    __table_args__ = (
        db.UniqueConstraint('user_id', 'name', name='uq_user_person'),
    )

    # ── One-to-Many Relationships ──────────────────────────────
    transactions = db.relationship('TransactionLog', backref='person', lazy='dynamic')
    hosted_events = db.relationship('Event', backref='host_person', lazy='dynamic',
                                    foreign_keys='Event.host_person_id')

    # ── Many-to-Many ───────────────────────────────────────────
    # Person ↔ Notes via NotePerson (see note_person.py)

    def __repr__(self):
        return f'<Person {self.person_id}: {self.name}>'
