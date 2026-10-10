"""
QuranAudio — surah audio metadata.
"""
from app.extensions import db


class QuranAudio(db.Model):
    __tablename__ = 'quran_audio'

    surah_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    surah_name = db.Column(db.String(100), nullable=False)
    surah_number = db.Column(db.Integer, nullable=False, unique=True)
    file_path = db.Column(db.String(500), nullable=False)
    duration_sec = db.Column(db.Integer, nullable=True)
    reciter_name = db.Column(db.String(100), nullable=True)
    language = db.Column(db.String(50), default='Arabic')
    total_verses = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    # ── One-to-Many ────────────────────────────────────────────
    listens = db.relationship('UserQuranListen', backref='surah', lazy='dynamic',
                              cascade='all, delete-orphan')

    def __repr__(self):
        return f'<QuranAudio {self.surah_number}: {self.surah_name}>'
