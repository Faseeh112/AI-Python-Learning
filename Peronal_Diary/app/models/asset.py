"""
Asset — valuable items with zakat, tax, and depreciation tracking.
Uses category_id instead of old asset_type column.
Currency is FK to currency table.
"""
from app.extensions import db
from datetime import datetime


class Asset(db.Model):
    __tablename__ = 'assets'

    asset_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id', ondelete='NO ACTION'),
                        nullable=True)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.category_id', ondelete='SET NULL'),
                            nullable=True)
    upload_id = db.Column(db.Integer,
                          db.ForeignKey('file_upload.upload_id', ondelete='NO ACTION'),
                          nullable=True)
    name = db.Column(db.String(200), nullable=False)
    acquired_from = db.Column(db.String(200), nullable=True)
    acquired_date = db.Column(db.Date, nullable=True)
    weight_grams = db.Column(db.Numeric(10, 2), nullable=True)
    purchase_value = db.Column(db.Numeric(12, 2), nullable=True)
    current_value = db.Column(db.Numeric(12, 2), nullable=True)
    currency = db.Column(db.String(3), db.ForeignKey('currency.code', ondelete='NO ACTION'),
                         default='PKR')
    is_zakatable = db.Column(db.Boolean, default=False)
    purpose = db.Column(db.String(20), default='personal')
    is_tax_asset = db.Column(db.Boolean, default=True)
    depreciation_rate = db.Column(db.Numeric(5, 4), default=0)
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

    # ── Constraints ────────────────────────────────────────────
    __table_args__ = (
        db.CheckConstraint("purpose IN ('personal','business','resale')", name='ck_asset_purpose'),
        db.CheckConstraint("weight_grams >= 0", name='ck_asset_weight'),
        db.CheckConstraint("purchase_value >= 0", name='ck_asset_purchase'),
        db.CheckConstraint("current_value >= 0", name='ck_asset_current'),
    )

    # ── Relationship to Currency ───────────────────────────────
    currency_ref = db.relationship('Currency', foreign_keys=[currency], lazy='joined')

    def __repr__(self):
        return f'<Asset {self.asset_id}: {self.name}>'
