"""
Category Routes — /api/categories
Category management — unified semantic type for items, assets, transactions.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

category_bp = Blueprint('categories', __name__, url_prefix='/api/categories')


@category_bp.route('', methods=['GET'])
def list_categories():
    # Purpose: List all active categories
    # Auth:    JWT required
    # Query:   ?is_zakatable=&tax_relevant=
    # Calls:   category_service.get_categories()
    # Returns: 200 with category list
    pass


@category_bp.route('', methods=['POST'])
def create_category():
    # Purpose: Create custom category
    # Auth:    JWT required (admin only)
    # Input:   { name, description, is_zakatable, default_depr_rate, tax_relevant, icon }
    # Calls:   category_service.create_category()
    # Returns: 201 with created category
    pass


@category_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    # Purpose: Update category properties
    # Auth:    JWT required (admin only)
    # Calls:   category_service.update_category()
    # Returns: 200 with updated category
    pass


@category_bp.route('/<int:category_id>/assets', methods=['GET'])
def get_category_assets(category_id):
    # Purpose: List all assets under a category
    # Auth:    JWT required
    # Query:   ?page=&per_page=
    # Calls:   category_service.get_category_assets()
    # Returns: 200 paginated
    pass
