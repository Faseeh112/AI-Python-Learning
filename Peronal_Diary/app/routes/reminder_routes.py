"""
Reminder Routes — /api/reminders
Scheduled alerts with recurrence, optionally linked to events.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

reminder_bp = Blueprint('reminders', __name__, url_prefix='/api/reminders')


@reminder_bp.route('', methods=['GET'])
def list_reminders():
    # Purpose: List reminders (filterable by done/pending, date)
    # Auth:    JWT required
    # Query:   ?page=&per_page=&is_done=&date_from=&date_to=
    # Calls:   reminder_service.get_reminders()
    # Returns: 200 paginated
    pass


@reminder_bp.route('', methods=['POST'])
def create_reminder():
    # Purpose: Create reminder (optionally linked to event)
    # Auth:    JWT required
    # Input:   { title, date_time, repeat_type, remind_before, notes, event_id }
    # Calls:   reminder_service.create_reminder()
    # Returns: 201 with created reminder
    pass


@reminder_bp.route('/<int:reminder_id>', methods=['PUT'])
def update_reminder(reminder_id):
    # Purpose: Update reminder
    # Auth:    JWT required + ownership check
    # Calls:   reminder_service.update_reminder()
    # Returns: 200 with updated reminder
    pass


@reminder_bp.route('/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    # Purpose: Soft-delete reminder (is_active = False)
    # Auth:    JWT required + ownership check
    # Calls:   reminder_service.soft_delete_reminder()
    # Returns: 200
    pass


@reminder_bp.route('/<int:reminder_id>/done', methods=['POST'])
def mark_done(reminder_id):
    # Purpose: Mark reminder as completed (is_done = True)
    # Auth:    JWT required + ownership check
    # Calls:   reminder_service.mark_done()
    # Returns: 200
    pass


@reminder_bp.route('/upcoming', methods=['GET'])
def get_upcoming():
    # Purpose: Get reminders due within next N hours
    # Auth:    JWT required
    # Query:   ?hours=24
    # Calls:   reminder_service.get_upcoming()
    # Returns: 200 with upcoming reminders
    pass
