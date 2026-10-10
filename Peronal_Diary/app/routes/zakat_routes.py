"""
Zakat Routes — /api/zakat
Zakat calculation, payment tracking, and summary.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

zakat_bp = Blueprint('zakat', __name__, url_prefix='/api/zakat')


@zakat_bp.route('/due', methods=['GET'])
def get_zakat_due():
    # Purpose: Calculate zakat due on eligible assets (mirrors vw_zakat_due)
    # Auth:    JWT required
    # Logic:   zakatable assets owned >= 354 days (Islamic lunar year)
    #          → 2.5% of current_value, check nisab threshold
    # Calls:   zakat_service.calculate_due()
    # Returns: 200 with [ { asset_name, current_value, zakat_due, days_owned } ]
    pass


@zakat_bp.route('/paid', methods=['GET'])
def get_zakat_paid():
    # Purpose: Zakat payments this year (mirrors vw_zakat_paid)
    # Auth:    JWT required
    # Query:   ?year=
    # Calls:   zakat_service.get_payments()
    # Returns: 200 with payment records
    pass


@zakat_bp.route('/summary', methods=['GET'])
def get_summary():
    # Purpose: Due vs paid vs remaining (mirrors vw_zakat_summary)
    # Auth:    JWT required
    # Calls:   zakat_service.get_summary()
    # Returns: 200 with { total_due, total_paid, remaining }
    pass


@zakat_bp.route('/pay', methods=['POST'])
def record_payment():
    # Purpose: Record zakat payment → creates transaction with Zakat category
    # Auth:    JWT required
    # Input:   { amount, person_id, currency, date, notes }
    # Logic:   lookup category_id for 'Zakat', direction = 'given'
    # Calls:   zakat_service.record_payment()
    # Returns: 201 with transaction record
    pass
