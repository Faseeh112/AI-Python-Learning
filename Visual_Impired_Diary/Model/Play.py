from Visual_Impired_Diary.db import db
from datetime import datetime


class Play(db.Model):
	__tablename__ = 'Play'  # Capital P

	play_id = db.Column(db.Integer, primary_key=True)  # lowercase 'play_id'
	Reminder_id = db.Column(db.Integer, db.ForeignKey("Reminders.Reminder_id"))
	Surah_id = db.Column(db.Integer, db.ForeignKey("Quran_Audio.Surah_id"))
	Remind_date = db.Column(db.Date)
	Remind_time = db.Column(db.Time)
	Repeat_type = db.Column(db.String(50))
	created_at = db.Column(db.DateTime, default=datetime.now)

	reminder_rship = db.relationship('Reminders', back_populates='play_rship')
	quran_rship = db.relationship('QuranAudio', back_populates='play_rship')
