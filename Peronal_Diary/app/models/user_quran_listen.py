"""
UserQuranListen — tracks user listening sessions for Quran surahs.
"""
from app.extensions import db
from datetime import datetime


class UserQuranListen(db.Model):
    __tablename__ = 'user_quran_listen'

    listen_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    surah_id = db.Column(db.Integer, db.ForeignKey('quran_audio.surah_id', ondelete='CASCADE'),
                         nullable=False)
    listened_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress_sec = db.Column(db.Integer, default=0)
    is_completed = db.Column(db.Boolean, default=False)
    device = db.Column(db.String(50), nullable=True)
    session_id = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<UserQuranListen user={self.user_id} surah={self.surah_id}>'
