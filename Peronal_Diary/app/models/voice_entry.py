"""
VoiceEntry — STT output with NLP metadata.
Linked to notes (optional) and feeds into knowledge triples.
"""
from app.extensions import db
from datetime import datetime


class VoiceEntry(db.Model):
    __tablename__ = 'voice_entry'

    voice_entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    notes_id = db.Column(db.Integer, db.ForeignKey('notes.notes_id', ondelete='NO ACTION'),
                         nullable=True)
    audio_path = db.Column(db.String(500), nullable=True)
    transcribed_txt = db.Column(db.Text, nullable=True)
    ner_output = db.Column(db.String(4000), nullable=True)
    intent = db.Column(db.String(20), nullable=True)
    duration_sec = db.Column(db.Integer, nullable=True)
    confidence = db.Column(db.Numeric(5, 2), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    model_used = db.Column(db.String(50), nullable=True)
    triples_extracted = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    # ── Constraints ────────────────────────────────────────────
    __table_args__ = (
        db.CheckConstraint(
            "intent IN ('store','query','update','delete','unknown')",
            name='ck_voice_intent'
        ),
    )

    # ── One-to-Many ────────────────────────────────────────────
    raw_text_logs = db.relationship('RawTextLog', backref='voice_entry', lazy='dynamic')
    knowledge_triples = db.relationship('KnowledgeTriple', backref='voice_entry', lazy='dynamic')

    def __repr__(self):
        return f'<VoiceEntry {self.voice_entry_id} intent={self.intent}>'
