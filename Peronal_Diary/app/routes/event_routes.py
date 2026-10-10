"""
Event Routes — /api/events
Event CRUD linked to host persons and locations.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

event_bp = Blueprint('events', __name__, url_prefix='/api/events')


@event_bp.route('', methods=['GET'])
def list_events():
    # Purpose: List events (filterable by date, type, completion)
    # Auth:    JWT required
    # Query:   ?page=&per_page=&event_type=&is_completed=&date_from=&date_to=
    # Calls:   event_service.get_events()
    # Returns: 200 paginated
    pass


@event_bp.route('', methods=['POST'])
def create_event():
    # Purpose: Create event with host person and location
    # Auth:    JWT required
    # Input:   { title, date, event_type, description, host_person_id, location_id }
    # Calls:   event_service.create_event()
    # Returns: 201 with created event
    pass


@event_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    # Purpose: Get event with reminders, transactions, host, location
    # Auth:    JWT required + ownership check
    # Calls:   event_service.get_event_detail()
    # Returns: 200 or 404
    pass


@event_bp.route('/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    # Purpose: Update event details
    # Auth:    JWT required + ownership check
    # Calls:   event_service.update_event()
    # Returns: 200 with updated event
    pass


@event_bp.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    # Purpose: Soft-delete event (is_active = False)
    # Auth:    JWT required + ownership check
    # Calls:   event_service.soft_delete_event()
    # Returns: 200
    pass
