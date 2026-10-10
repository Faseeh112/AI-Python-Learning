"""
Attachment — files attached to notes.
Includes SHA-256 file_hash for integrity and proper MIME type.
"""
from app.extensions import db
from datetime import datetime


class Attachment(db.Model):
    __tablename__ = 'attachment'

    attachment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    notes_id = db.Column(db.Integer, db.ForeignKey('notes.notes_id', ondelete='NO ACTION'),
                         nullable=True)
    title = db.Column(db.String(200), nullable=True)
    type = db.Column(db.String(50), nullable=True)
    file_path = db.Column(db.String(500), nullable=True)
    file_hash = db.Column(db.LargeBinary(32), nullable=True)       # SHA-256
    mime_type = db.Column(db.String(100), nullable=True)
    text_content = db.Column(db.String(4000), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # ── Constraints ────────────────────────────────────────────
    __table_args__ = (
        db.CheckConstraint(
            "type IN ('image','pdf','audio','video','other')",
            name='ck_attachment_type'
        ),
    )

    def __repr__(self):
        return f'<Attachment {self.attachment_id}: {self.title}>'
