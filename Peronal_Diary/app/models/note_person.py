"""
NotePerson — junction table for Notes ↔ Person many-to-many.
Includes role attribute to describe the relationship context.
"""
from app.extensions import db
from datetime import datetime


class NotePerson(db.Model):
    __tablename__ = 'note_person'

    notes_id = db.Column(db.Integer, db.ForeignKey('notes.notes_id', ondelete='CASCADE'),
                         primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id', ondelete='NO ACTION'),
                          primary_key=True)
    role = db.Column(db.String(30), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    context_notes = db.Column(db.String(200), nullable=True)
    verified = db.Column(db.Boolean, default=False)

    # ── Constraints ────────────────────────────────────────────
    __table_args__ = (
        db.CheckConstraint(
            "role IN ('event_owner','met_at_event','mentioned','recipient','sender','other')",
            name='ck_noteperson_role'
        ),
    )

    def __repr__(self):
        return f'<NotePerson note={self.notes_id} person={self.person_id} role={self.role}>'
