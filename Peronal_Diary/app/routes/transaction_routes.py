"""
Transaction Routes — /api/transactions
Financial transaction CRUD with category-based classification.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

transaction_bp = Blueprint('transactions', __name__, url_prefix='/api/transactions')


@transaction_bp.route('', methods=['GET'])
def list_transactions():
    # Purpose: List transactions (filterable by category, person, direction, date range)
    # Auth:    JWT required
    # Query:   ?page=&per_page=&category_id=&person_id=&direction=&date_from=&date_to=&currency=
    # Calls:   transaction_service.get_transactions()
    # Returns: 200 paginated
    pass


@transaction_bp.route('', methods=['POST'])
def create_transaction():
    # Purpose: Create transaction with category, person, amount, direction
    # Auth:    JWT required
    # Input:   { category_id, person_id, amount, direction, date, currency, notes, item_id, event_id }
    # Calls:   transaction_service.create_transaction()
    # Returns: 201 with created transaction
    pass


@transaction_bp.route('/<int:trans_id>', methods=['GET'])
def get_transaction(trans_id):
    # Purpose: Get single transaction with category + person details
    # Auth:    JWT required + ownership check
    # Calls:   transaction_service.get_transaction_detail()
    # Returns: 200 or 404
    pass


@transaction_bp.route('/<int:trans_id>', methods=['PUT'])
def update_transaction(trans_id):
    # Purpose: Update transaction fields
    # Auth:    JWT required + ownership check
    # Calls:   transaction_service.update_transaction()
    # Returns: 200 with updated transaction
    pass


@transaction_bp.route('/<int:trans_id>', methods=['DELETE'])
def delete_transaction(trans_id):
    # Purpose: Soft-delete transaction (is_active = False)
    # Auth:    JWT required + ownership check
    # Calls:   transaction_service.soft_delete_transaction()
    # Returns: 200
    pass


@transaction_bp.route('/summary', methods=['GET'])
def get_summary():
    # Purpose: Aggregate summary by category/direction/period
    # Auth:    JWT required
    # Query:   ?group_by=category|direction|month&date_from=&date_to=
    # Calls:   transaction_service.get_summary()
    # Returns: 200 with aggregated data
    pass
