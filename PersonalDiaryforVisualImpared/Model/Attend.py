from PersonalDiaryforVisualImpared.db import db


class Attend(db.Model):
    __tablename__ = 'Attend'
    Attend_id = db.Column(db.Integer, primary_key=True)

    User_id = db.Column(db.Integer, db.ForeignKey("User.User_id"))
    Event_id = db.Column(db.Integer, db.ForeignKey("Event.Event_id"))
    Detail_event_id = db.Column(db.Integer, db.ForeignKey("Detail_event.Detail_event_id"))

    user_rship = db.relationship('User', back_populates='attend_rship')
    event_rship = db.relationship('Event', back_populates='attend_rship')
    detail_rship = db.relationship('Detail_event', back_populates='attend_rship')