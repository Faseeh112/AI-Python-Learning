"""
Tax Routes — /api/tax
Tax asset reporting and depreciation summaries.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

tax_bp = Blueprint('tax', __name__, url_prefix='/api/tax')


@tax_bp.route('/assets', methods=['GET'])
def get_tax_assets():
    # Purpose: Tax-relevant assets with depreciation info (mirrors vw_tax_assets)
    # Auth:    JWT required
    # Calls:   tax_service.get_tax_assets()
    # Returns: 200 with [ { name, category, purpose, purchase_value, current_value,
    #                        this_yr_depr, next_yr_value, depreciation_rate } ]
    pass


@tax_bp.route('/report', methods=['GET'])
def generate_report():
    # Purpose: Generate annual tax asset report
    # Auth:    JWT required
    # Query:   ?year=
    # Calls:   tax_service.generate_tax_report()
    # Returns: 200 with full tax report data
    pass
