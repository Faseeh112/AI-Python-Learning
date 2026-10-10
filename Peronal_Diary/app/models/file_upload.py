"""
FileUpload — uploaded files with extraction pipeline tracking.
Tracks OCR/NLP processing status and counts of created records.
"""
from app.extensions import db
from datetime import datetime


class FileUpload(db.Model):
    __tablename__ = 'file_upload'

    upload_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    notes_id = db.Column(db.Integer, db.ForeignKey('notes.notes_id', ondelete='NO ACTION'),
                         nullable=True)
    original_filename = db.Column(db.String(300), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size_kb = db.Column(db.Integer, nullable=True)
    file_hash = db.Column(db.LargeBinary(32), nullable=True)       # SHA-256
    mime_type = db.Column(db.String(100), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by = db.Column(db.String(20), default='user')
    extraction_status = db.Column(db.String(20), default='pending')
    extracted_text = db.Column(db.Text, nullable=True)
    extracted_at = db.Column(db.DateTime, nullable=True)
    extraction_error = db.Column(db.String(500), nullable=True)
    ner_output = db.Column(db.String(4000), nullable=True)
    is_nlp_processed = db.Column(db.Boolean, default=False)
    summary = db.Column(db.String(1000), nullable=True)
    page_count = db.Column(db.Integer, nullable=True)
    sheet_count = db.Column(db.Integer, nullable=True)
    row_count = db.Column(db.Integer, nullable=True)
    word_count = db.Column(db.Integer, nullable=True)
    language = db.Column(db.String(20), nullable=True)
    notes_created = db.Column(db.Integer, default=0)
    transactions_created = db.Column(db.Integer, default=0)
    documents_created = db.Column(db.Integer, default=0)
    assets_created = db.Column(db.Integer, default=0)
    triples_extracted = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    # ── Constraints ────────────────────────────────────────────
    __table_args__ = (
        db.CheckConstraint(
            "file_type IN ('pdf','docx','xlsx','csv','txt','jpg','png','mp3','other')",
            name='ck_upload_filetype'
        ),
        db.CheckConstraint(
            "uploaded_by IN ('user','system','nlp')",
            name='ck_upload_by'
        ),
        db.CheckConstraint(
            "extraction_status IN ('pending','processing','done','failed','skipped')",
            name='ck_upload_status'
        ),
        db.CheckConstraint("file_size_kb >= 0", name='ck_upload_size'),
    )

    # ── One-to-Many ────────────────────────────────────────────
    documents = db.relationship('Document', backref='upload', lazy='dynamic')
    transactions = db.relationship('TransactionLog', backref='upload', lazy='dynamic')
    assets = db.relationship('Asset', backref='upload', lazy='dynamic')
    raw_text_logs = db.relationship('RawTextLog', backref='upload', lazy='dynamic')
    knowledge_triples = db.relationship('KnowledgeTriple', backref='upload', lazy='dynamic')

    def __repr__(self):
        return f'<FileUpload {self.upload_id}: {self.original_filename}>'
