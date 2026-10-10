"""
Notes — core diary entries.
Linked to tags (M2M), persons (M2M), voice entries, attachments, uploads.
"""
from app.extensions import db
from app.models.note_tag import note_tag
from datetime import datetime


class Notes(db.Model):
    __tablename__ = 'notes'

    notes_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    title = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(4000), nullable=True)
    note_type = db.Column(db.String(20), default='text')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    is_processed = db.Column(db.Boolean, default=False)
    sentiment = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    # ── Constraints ────────────────────────────────────────────
    __table_args__ = (
        db.CheckConstraint(
            "note_type IN ('voice','text','mixed','file')",
            name='ck_notes_type'
        ),
    )

    # ── Many-to-Many: Notes ↔ Tag ──────────────────────────────
    tags = db.relationship('Tag', secondary=note_tag, lazy='subquery',
                           backref=db.backref('notes', lazy='dynamic'))

    # ── Many-to-Many: Notes ↔ Person ───────────────────────────
    note_persons = db.relationship('NotePerson', backref='note', lazy='dynamic',
                                   cascade='all, delete-orphan')

    # ── One-to-Many ────────────────────────────────────────────
    voice_entries = db.relationship('VoiceEntry', backref='note', lazy='dynamic')
    attachments = db.relationship('Attachment', backref='note', lazy='dynamic')
    file_uploads = db.relationship('FileUpload', backref='note', lazy='dynamic')
    knowledge_triples = db.relationship('KnowledgeTriple', backref='note', lazy='dynamic')

    def __repr__(self):
        return f'<Notes {self.notes_id}: {self.title}>'
