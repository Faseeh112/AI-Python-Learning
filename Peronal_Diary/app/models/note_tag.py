"""
NoteTag — junction table for Notes ↔ Tag many-to-many.
"""
from app.extensions import db

note_tag = db.Table(
    'note_tag',
    db.Column('notes_id', db.Integer, db.ForeignKey('notes.notes_id', ondelete='CASCADE'),
              primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id', ondelete='CASCADE'),
              primary_key=True),
)
