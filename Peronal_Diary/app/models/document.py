"""
Document — education, medical, legal, financial documents with expiry tracking.
"""
from app.extensions import db
from datetime import datetime


class Document(db.Model):
    __tablename__ = 'document'

    doc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id', ondelete='NO ACTION'),
                        nullable=True)
    location_id = db.Column(db.Integer,
                            db.ForeignKey('location.location_id', ondelete='NO ACTION'),
                            nullable=True)
    upload_id = db.Column(db.Integer,
                          db.ForeignKey('file_upload.upload_id', ondelete='NO ACTION'),
                          nullable=True)
    name = db.Column(db.String(200), nullable=False)
    doc_type = db.Column(db.String(100), nullable=True)
    sub_type = db.Column(db.String(100), nullable=True)
    issuer = db.Column(db.String(200), nullable=True)
    issue_date = db.Column(db.Date, nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)
    scanned_copy = db.Column(db.String(500), nullable=True)
    notes = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # ── Constraints ────────────────────────────────────────────
    __table_args__ = (
        db.CheckConstraint(
            "doc_type IN ('education','medical','legal','personal','financial','other')",
            name='ck_document_type'
        ),
    )

    def __repr__(self):
        return f'<Document {self.doc_id}: {self.name}>'
