"""
Currency reference table.
Stores ISO 4217 currency codes used across transactions and assets.
"""
from app.extensions import db


class Currency(db.Model):
    __tablename__ = 'currency'

    code = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # ── Relationships ──────────────────────────────────────────
    # Referenced by Asset.currency and TransactionLog.currency via FK
    # No backref needed — accessed via join

    def __repr__(self):
        return f'<Currency {self.code}>'
