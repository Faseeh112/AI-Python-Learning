"""
Tag Routes — /api/tags
Tag management and autocomplete search.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

tag_bp = Blueprint('tags', __name__, url_prefix='/api/tags')


@tag_bp.route('', methods=['GET'])
def list_tags():
    # Purpose: List all tags (for autocomplete dropdowns)
    # Auth:    JWT required
    # Calls:   tag_service.get_tags()
    # Returns: 200 with tag list
    pass


@tag_bp.route('', methods=['POST'])
def create_tag():
    # Purpose: Create a new tag
    # Auth:    JWT required
    # Input:   { name }
    # Calls:   tag_service.create_tag()
    # Returns: 201 with created tag
    pass


@tag_bp.route('/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    # Purpose: Delete unused tag
    # Auth:    JWT required
    # Calls:   tag_service.delete_tag()
    # Returns: 200
    pass


@tag_bp.route('/search', methods=['GET'])
def search_tags():
    # Purpose: Autocomplete search for tags (LIKE query)
    # Auth:    JWT required
    # Query:   ?q=
    # Calls:   tag_service.search_tags()
    # Returns: 200 with matching tags
    pass
