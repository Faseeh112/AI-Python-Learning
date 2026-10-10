"""
RawTextLog — NLP pipeline input buffer.
Stores raw text from voice, text, or file_extract sources for processing.
"""
from app.extensions import db
from datetime import datetime


class RawTextLog(db.Model):
    __tablename__ = 'raw_text_log'

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    raw_text = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(15), nullable=False)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_processed = db.Column(db.Boolean, default=False)
    voice_entry_id = db.Column(db.Integer,
                               db.ForeignKey('voice_entry.voice_entry_id', ondelete='NO ACTION'),
                               nullable=True)
    upload_id = db.Column(db.Integer,
                          db.ForeignKey('file_upload.upload_id', ondelete='NO ACTION'),
                          nullable=True)
    language = db.Column(db.String(10), default='en')
    error_msg = db.Column(db.String(500), nullable=True)
    nlp_version = db.Column(db.String(20), nullable=True)

    # ── Constraints ────────────────────────────────────────────
    __table_args__ = (
        db.CheckConstraint(
            "source IN ('voice','text','file_extract')",
            name='ck_rawlog_source'
        ),
    )

    def __repr__(self):
        return f'<RawTextLog {self.log_id} source={self.source}>'
