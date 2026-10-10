"""
TransactionLog — financial transactions (given/received).
Uses category_id instead of old trans_type column.
Currency is FK to currency table.
"""
from app.extensions import db
from datetime import datetime, date


class TransactionLog(db.Model):
    __tablename__ = 'transaction_log'

    trans_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'),
                        nullable=False)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.category_id', ondelete='NO ACTION'),
                            nullable=False)
    person_id = db.Column(db.Integer,
                          db.ForeignKey('person.person_id', ondelete='NO ACTION'),
                          nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id', ondelete='NO ACTION'),
                        nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id', ondelete='NO ACTION'),
                         nullable=True)
    upload_id = db.Column(db.Integer,
                          db.ForeignKey('file_upload.upload_id', ondelete='NO ACTION'),
                          nullable=True)
    direction = db.Column(db.String(10), default='given')
    amount = db.Column(db.Numeric(12, 2), nullable=True)
    date = db.Column(db.Date, default=date.today)
    currency = db.Column(db.String(3), db.ForeignKey('currency.code', ondelete='NO ACTION'),
                         default='PKR')
    involvement = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # ── Constraints ────────────────────────────────────────────
    __table_args__ = (
        db.CheckConstraint("direction IN ('given','received')", name='ck_trans_direction'),
        db.CheckConstraint("amount >= 0", name='ck_trans_amount_positive'),
    )

    # ── Relationship to Currency ───────────────────────────────
    currency_ref = db.relationship('Currency', foreign_keys=[currency], lazy='joined')

    def __repr__(self):
        return f'<TransactionLog {self.trans_id} {self.direction} {self.amount}>'
