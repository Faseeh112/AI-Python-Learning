from PersonalDiaryforVisualImpared.db import db
from datetime import datetime


class Play(db.Model):
    __tablename__ = 'Play'
    play_id = db.Column(db.Integer, primary_key=True)
    Play_date = db.Column(db.Date)
    Play_time = db.Column(db.Time)
    Repeat_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)

    User_id = db.Column(db.Integer, db.ForeignKey("User.User_id"))
    Audio_id = db.Column(db.Integer, db.ForeignKey("Quran_Audio.Audio_id"))

    user_rship = db.relationship('User', back_populates='play_rship')
    audio_rship = db.relationship('Quran_Audio', back_populates='play_rship')