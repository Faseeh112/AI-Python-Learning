"""
Person Routes — /api/persons
Contact/relation management.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

person_bp = Blueprint('persons', __name__, url_prefix='/api/persons')


@person_bp.route('', methods=['GET'])
def list_persons():
    # Purpose: List user contacts (paginated, searchable)
    # Auth:    JWT required
    # Query:   ?page=&per_page=&search=&relation=
    # Calls:   person_service.get_persons()
    # Returns: 200 paginated
    pass


@person_bp.route('', methods=['POST'])
def create_person():
    # Purpose: Create new contact
    # Auth:    JWT required
    # Input:   { name, relation, phone, notes }
    # Calls:   person_service.create_person()
    # Returns: 201 with created person
    pass


@person_bp.route('/<int:person_id>', methods=['GET'])
def get_person(person_id):
    # Purpose: Get person with linked notes, transactions, events
    # Auth:    JWT required + ownership check
    # Calls:   person_service.get_person_detail()
    # Returns: 200 or 404
    pass


@person_bp.route('/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    # Purpose: Update person details
    # Auth:    JWT required + ownership check
    # Calls:   person_service.update_person()
    # Returns: 200 with updated person
    pass


@person_bp.route('/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    # Purpose: Soft-delete person (is_active = False)
    # Auth:    JWT required + ownership check
    # Calls:   person_service.soft_delete_person()
    # Returns: 200
    pass
