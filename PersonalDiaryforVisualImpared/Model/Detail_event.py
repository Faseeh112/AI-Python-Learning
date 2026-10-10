from PersonalDiaryforVisualImpared.db import db
from datetime import datetime

class Detail_event(db.Model):
    __tablename__ = 'Detail_event'
    Detail_event_id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255))
    Context = db.Column(db.Text)
    Transaction_Type = db.Column(db.String(50))
    Date = db.Column(db.Date)
    Transaction = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)

    attend_rship = db.relationship('Attend', back_populates='detail_rship')