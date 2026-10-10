"""
Reminder — scheduled alerts, optionally linked to events.
"""
from app.extensions import db
from datetime import datetime


class Reminder(db.Model):
    __tablename__ = 'reminder'

    reminder_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id', ondelete='NO ACTION'),
                         nullable=True)
    title = db.Column(db.String(200), nullable=False)
    date_time = db.Column(db.DateTime, nullable=True)
    repeat_type = db.Column(db.String(50), default='None')
    is_done = db.Column(db.Boolean, default=False)
    remind_before = db.Column(db.Integer, default=60)  # minutes
    notes = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # ── Constraints ────────────────────────────────────────────
    __table_args__ = (
        db.CheckConstraint(
            "repeat_type IN ('None','Daily','Weekly','Monthly','Yearly')",
            name='ck_reminder_repeat'
        ),
    )

    def __repr__(self):
        return f'<Reminder {self.reminder_id}: {self.title}>'
