from Visual_Impired_Diary.db import db


class QuranAudio(db.Model):
	__tablename__ = 'Quran_Audio'  # underscore between Quran and Audio

	Surah_id = db.Column(db.Integer, primary_key=True)  # Changed from 'id'
	Surah_name = db.Column(db.String(150))  # Capital S
	reciter_name = db.Column(db.String(150))  # lowercase 'r'
	file_path = db.Column(db.String(255))  # lowercase 'f'
	duration = db.Column(db.String(50))  # lowercase 'd'

	play_rship = db.relationship('Play', back_populates='quran_rship')
