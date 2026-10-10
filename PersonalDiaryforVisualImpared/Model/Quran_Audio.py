from PersonalDiaryforVisualImpared.db import db

class Quran_Audio(db.Model):
    __tablename__ = 'Quran_Audio'
    Audio_id = db.Column(db.Integer, primary_key=True)
    Surah_id = db.Column(db.Integer)
    Surah_name = db.Column(db.String(255))
    reciter_name = db.Column(db.String(255))
    Audio_data = db.Column(db.LargeBinary)
    duration = db.Column(db.String(50))

    play_rship = db.relationship('Play', back_populates='audio_rship')