"""
Location Routes — /api/locations
Hierarchical location management with tree operations.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

location_bp = Blueprint('locations', __name__, url_prefix='/api/locations')


@location_bp.route('', methods=['GET'])
def list_locations():
    # Purpose: List user locations (optionally as tree structure)
    # Auth:    JWT required
    # Query:   ?page=&per_page=&tree=true|false
    # Calls:   location_service.get_locations()
    # Returns: 200 paginated or tree structure
    pass


@location_bp.route('', methods=['POST'])
def create_location():
    # Purpose: Create location (optionally under a parent)
    # Auth:    JWT required
    # Input:   { name, parent_location_id, additional_info }
    # Calls:   location_service.create_location()
    # Returns: 201 with created location
    pass


@location_bp.route('/<int:location_id>', methods=['GET'])
def get_location(location_id):
    # Purpose: Get location with children and linked items/events
    # Auth:    JWT required + ownership check
    # Calls:   location_service.get_location_detail()
    # Returns: 200 or 404
    pass


@location_bp.route('/<int:location_id>', methods=['PUT'])
def update_location(location_id):
    # Purpose: Update location (name, parent, info)
    # Auth:    JWT required + ownership check
    # Calls:   location_service.update_location()
    # Returns: 200 with updated location
    pass


@location_bp.route('/<int:location_id>', methods=['DELETE'])
def delete_location(location_id):
    # Purpose: Soft-delete location (is_active = False)
    # Auth:    JWT required + ownership check
    # Calls:   location_service.soft_delete_location()
    # Returns: 200
    pass


@location_bp.route('/<int:location_id>/tree', methods=['GET'])
def get_subtree(location_id):
    # Purpose: Get full hierarchy under this location (recursive)
    # Auth:    JWT required + ownership check
    # Calls:   location_service.get_subtree()
    # Returns: 200 with nested tree structure
    pass
