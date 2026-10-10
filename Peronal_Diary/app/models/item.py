"""
Item — generic trackable object.
Uses category_id instead of old Type column (Fix #1).
"""
from app.extensions import db
from datetime import datetime


class Item(db.Model):
    __tablename__ = 'item'

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.category_id', ondelete='SET NULL'),
                            nullable=True)
    location_id = db.Column(db.Integer,
                            db.ForeignKey('location.location_id', ondelete='NO ACTION'),
                            nullable=True)
    name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # ── One-to-Many ────────────────────────────────────────────
    assets = db.relationship('Asset', backref='item', lazy='dynamic')
    documents = db.relationship('Document', backref='item', lazy='dynamic')
    transactions = db.relationship('TransactionLog', backref='item', lazy='dynamic')

    def __repr__(self):
        return f'<Item {self.item_id}: {self.name}>'
