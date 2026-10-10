"""
Category — unified semantic type.
Single source of truth replacing old Asset_type / Trans_type columns.
Drives zakat eligibility, depreciation rates, and tax relevance.
"""
from app.extensions import db
from datetime import datetime


class Category(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=True)
    is_zakatable = db.Column(db.Boolean, default=False)
    default_depr_rate = db.Column(db.Numeric(5, 4), default=0)
    tax_relevant = db.Column(db.Boolean, default=False)
    icon = db.Column(db.String(50), nullable=True)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ── One-to-Many Relationships ──────────────────────────────
    items = db.relationship('Item', backref='category', lazy='dynamic')
    transactions = db.relationship('TransactionLog', backref='category', lazy='dynamic')
    assets = db.relationship('Asset', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.category_id}: {self.name}>'
