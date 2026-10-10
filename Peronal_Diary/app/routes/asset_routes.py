"""
Asset Routes — /api/assets
Asset CRUD with zakat, tax, depreciation, and net worth endpoints.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

asset_bp = Blueprint('assets', __name__, url_prefix='/api/assets')


@asset_bp.route('', methods=['GET'])
def list_assets():
    # Purpose: List assets (filterable by category, zakatable, purpose)
    # Auth:    JWT required
    # Query:   ?page=&per_page=&category_id=&is_zakatable=&purpose=
    # Calls:   asset_service.get_assets()
    # Returns: 200 paginated
    pass


@asset_bp.route('', methods=['POST'])
def create_asset():
    # Purpose: Create asset — auto zakat/depreciation from category
    # Auth:    JWT required
    # Input:   { name, category_id, purchase_value, purpose, acquired_from,
    #            acquired_date, weight_grams, currency, upload_id }
    # Logic:   category lookup → set is_zakatable, depreciation_rate
    #          if Vehicle + resale → override is_zakatable = True
    # Calls:   asset_service.create_asset()
    # Returns: 201 with created asset
    pass


@asset_bp.route('/<int:asset_id>', methods=['GET'])
def get_asset(asset_id):
    # Purpose: Get single asset with category details
    # Auth:    JWT required + ownership check
    # Calls:   asset_service.get_asset_detail()
    # Returns: 200 or 404
    pass


@asset_bp.route('/<int:asset_id>', methods=['PUT'])
def update_asset(asset_id):
    # Purpose: Update asset fields (value, purpose, etc.)
    # Auth:    JWT required + ownership check
    # Calls:   asset_service.update_asset()
    # Returns: 200 with updated asset
    pass


@asset_bp.route('/<int:asset_id>', methods=['DELETE'])
def delete_asset(asset_id):
    # Purpose: Soft-delete asset (is_active = False)
    # Auth:    JWT required + ownership check
    # Calls:   asset_service.soft_delete_asset()
    # Returns: 200
    pass


@asset_bp.route('/net-worth', methods=['GET'])
def get_net_worth():
    # Purpose: Net worth breakdown by category (mirrors vw_net_worth)
    # Auth:    JWT required
    # Query:   ?currency=
    # Calls:   asset_service.calculate_net_worth()
    # Returns: 200 with { categories: [...], total }
    pass


@asset_bp.route('/depreciate', methods=['POST'])
def run_depreciation():
    # Purpose: Trigger annual depreciation update (mirrors sp_update_depreciation)
    # Auth:    JWT required (admin or scheduled job)
    # Calls:   asset_service.apply_depreciation()
    # Returns: 200 with { assets_updated: count }
    pass
