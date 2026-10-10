"""
KnowledgeTriple — typed subject-predicate-object triples.
Polymorphic FKs: subject_id/object_id reference different tables
based on subject_type/object_type. Integrity enforced at app layer.
"""
from app.extensions import db
from datetime import datetime


class KnowledgeTriple(db.Model):
    __tablename__ = 'knowledge_triple'

    triple_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    voice_entry_id = db.Column(db.Integer,
                               db.ForeignKey('voice_entry.voice_entry_id', ondelete='NO ACTION'),
                               nullable=True)
    upload_id = db.Column(db.Integer,
                          db.ForeignKey('file_upload.upload_id', ondelete='NO ACTION'),
                          nullable=True)
    notes_id = db.Column(db.Integer, db.ForeignKey('notes.notes_id', ondelete='NO ACTION'),
                         nullable=True)

    # ── Subject (typed entity reference) ───────────────────────
    subject_text = db.Column(db.String(200), nullable=False)
    subject_id = db.Column(db.Integer, nullable=True)
    subject_type = db.Column(db.String(50), nullable=True)

    # ── Predicate ──────────────────────────────────────────────
    predicate = db.Column(db.String(100), nullable=False)

    # ── Object (typed entity reference) ────────────────────────
    object_text = db.Column(db.String(500), nullable=False)
    object_id = db.Column(db.Integer, nullable=True)
    object_type = db.Column(db.String(50), nullable=True)

    confidence = db.Column(db.Numeric(5, 4), nullable=True)
    context_notes = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # ── Constraints ────────────────────────────────────────────
    __table_args__ = (
        db.CheckConstraint(
            "subject_type IN ('person','item','asset','location','event','document','user') "
            "OR subject_type IS NULL",
            name='ck_ktriple_subject_type'
        ),
        db.CheckConstraint(
            "object_type IN ('person','item','asset','location','event','document','user') "
            "OR object_type IS NULL",
            name='ck_ktriple_object_type'
        ),
    )

    # NOTE: subject_id/object_id are polymorphic FKs.
    # Referential integrity is enforced at the application layer
    # based on subject_type/object_type values.

    def __repr__(self):
        return f'<KnowledgeTriple {self.triple_id}: {self.subject_text} → {self.predicate} → {self.object_text}>'
