"""
Document Routes — /api/documents
Document CRUD with expiry tracking.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

document_bp = Blueprint('documents', __name__, url_prefix='/api/documents')


@document_bp.route('', methods=['GET'])
def list_documents():
    # Purpose: List documents (filterable by doc_type, expiry)
    # Auth:    JWT required
    # Query:   ?page=&per_page=&doc_type=&expiring_within_days=
    # Calls:   document_service.get_documents()
    # Returns: 200 paginated
    pass


@document_bp.route('', methods=['POST'])
def create_document():
    # Purpose: Create document record
    # Auth:    JWT required
    # Input:   { name, doc_type, sub_type, issuer, issue_date, expiry_date,
    #            item_id, location_id, upload_id, scanned_copy, notes }
    # Calls:   document_service.create_document()
    # Returns: 201 with created document
    pass


@document_bp.route('/<int:doc_id>', methods=['GET'])
def get_document(doc_id):
    # Purpose: Get document detail with item, location, upload info
    # Auth:    JWT required + ownership check
    # Calls:   document_service.get_document_detail()
    # Returns: 200 or 404
    pass


@document_bp.route('/<int:doc_id>', methods=['PUT'])
def update_document(doc_id):
    # Purpose: Update document
    # Auth:    JWT required + ownership check
    # Calls:   document_service.update_document()
    # Returns: 200 with updated document
    pass


@document_bp.route('/<int:doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    # Purpose: Soft-delete document (is_active = False)
    # Auth:    JWT required + ownership check
    # Calls:   document_service.soft_delete_document()
    # Returns: 200
    pass


@document_bp.route('/expiring', methods=['GET'])
def get_expiring():
    # Purpose: Documents expiring within 90 days (mirrors vw_expiring_docs)
    # Auth:    JWT required
    # Query:   ?days=90
    # Calls:   document_service.get_expiring()
    # Returns: 200 with expiring documents + days_left
    pass
