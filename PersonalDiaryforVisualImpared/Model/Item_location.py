from PersonalDiaryforVisualImpared.db import db
from datetime import datetime

class Item_location(db.Model):
    __tablename__ = 'Item_location'
    Loc_id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(255))
    Category = db.Column(db.String(255))
    Description = db.Column(db.Text)
    Location = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)

    User_id = db.Column(db.Integer, db.ForeignKey("User.User_id"))
    user_rship = db.relationship('User', back_populates='item_location_rship')