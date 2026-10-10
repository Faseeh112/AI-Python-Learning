"""
User Routes — /api/users
Profile management and account operations.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

user_bp = Blueprint('users', __name__, url_prefix='/api/users')


@user_bp.route('/me', methods=['GET'])
def get_profile():
    # Purpose: Get current user profile (excludes password_hash)
    # Auth:    JWT required
    # Calls:   user_service.get_user_profile()
    # Returns: 200 with user data
    pass


@user_bp.route('/me', methods=['PUT'])
def update_profile():
    # Purpose: Update name, language, timezone, profile_notes
    # Auth:    JWT required
    # Calls:   user_service.update_profile()
    # Returns: 200 with updated user
    pass


@user_bp.route('/me', methods=['DELETE'])
def deactivate_account():
    # Purpose: Soft-delete user account (is_active = False)
    # Auth:    JWT required
    # Calls:   user_service.soft_delete_user()
    # Returns: 200
    pass


@user_bp.route('/me/password', methods=['PUT'])
def change_password():
    # Purpose: Change password (requires current password)
    # Auth:    JWT required
    # Input:   { current_password, new_password }
    # Calls:   auth_service.change_password()
    # Returns: 200 or 400/401
    pass
