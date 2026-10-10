"""
Location — hierarchical location tree.
Self-referential FK allows: Country → City → Area → Building → Room.
"""
from app.extensions import db
from datetime import datetime


class Location(db.Model):
    __tablename__ = 'location'

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    name = db.Column(db.String(100), nullable=False)
    parent_location_id = db.Column(db.Integer,
                                   db.ForeignKey('location.location_id', ondelete='NO ACTION'),
                                   nullable=True)
    additional_info = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # ── Self-Referential Relationship ──────────────────────────
    children = db.relationship('Location', backref=db.backref('parent', remote_side=[location_id]),
                               lazy='dynamic')

    # ── One-to-Many ────────────────────────────────────────────
    items = db.relationship('Item', backref='location', lazy='dynamic')
    events = db.relationship('Event', backref='location', lazy='dynamic')
    documents = db.relationship('Document', backref='location', lazy='dynamic')

    def __repr__(self):
        return f'<Location {self.location_id}: {self.name}>'
