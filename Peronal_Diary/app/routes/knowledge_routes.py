"""
Knowledge Routes — /api/knowledge
Knowledge triple CRUD and graph traversal.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

knowledge_bp = Blueprint('knowledge', __name__, url_prefix='/api/knowledge')


@knowledge_bp.route('', methods=['GET'])
def list_triples():
    # Purpose: List knowledge triples (filterable by predicate, type)
    # Auth:    JWT required
    # Query:   ?page=&per_page=&predicate=&subject_type=&object_type=
    # Calls:   knowledge_service.get_triples()
    # Returns: 200 paginated
    pass


@knowledge_bp.route('', methods=['POST'])
def create_triple():
    # Purpose: Manually create a knowledge triple
    # Auth:    JWT required
    # Input:   { subject_text, subject_type, subject_id, predicate,
    #            object_text, object_type, object_id, confidence, context_notes }
    # Calls:   knowledge_service.create_triple()
    # Returns: 201 with created triple
    pass


@knowledge_bp.route('/<int:triple_id>', methods=['GET'])
def get_triple(triple_id):
    # Purpose: Get triple with resolved entity references
    # Auth:    JWT required + ownership check
    # Calls:   knowledge_service.get_triple_detail()
    # Returns: 200 or 404
    pass


@knowledge_bp.route('/<int:triple_id>', methods=['DELETE'])
def delete_triple(triple_id):
    # Purpose: Soft-delete triple (is_active = False)
    # Auth:    JWT required + ownership check
    # Calls:   knowledge_service.soft_delete_triple()
    # Returns: 200
    pass


@knowledge_bp.route('/graph/<string:entity_type>/<int:entity_id>', methods=['GET'])
def get_entity_graph(entity_type, entity_id):
    # Purpose: Get all triples where entity appears as subject or object
    # Auth:    JWT required
    # Calls:   knowledge_service.get_entity_graph()
    # Returns: 200 with related triples
    pass


@knowledge_bp.route('/search', methods=['GET'])
def search_triples():
    # Purpose: Search triples by subject/object text
    # Auth:    JWT required
    # Query:   ?q=&page=&per_page=
    # Calls:   knowledge_service.search_triples()
    # Returns: 200 with matching triples
    pass
