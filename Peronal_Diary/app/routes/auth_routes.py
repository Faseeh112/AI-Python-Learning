"""
Auth Routes — /api/auth
Registration, login, token management, password reset.
"""
from flask import Blueprint, request
from app.utils.response_helpers import success_response, error_response

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    # Purpose: Register new user account
    # Input:   { name, email, password }
    # Calls:   auth_service.register_user()
    # Returns: 201 with user_id or 400/409
    pass


@auth_bp.route('/login', methods=['POST'])
def login():
    # Purpose: Authenticate user and return JWT tokens
    # Input:   { email, password }
    # Calls:   auth_service.authenticate_user()
    # Returns: 200 with { access_token, refresh_token } or 401
    pass


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    # Purpose: Refresh expired access token
    # Input:   refresh_token in Authorization header
    # Calls:   auth_service.refresh_access_token()
    # Returns: 200 with new access_token or 401
    pass


@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Purpose: Invalidate current token (blacklist)
    # Input:   access_token in Authorization header
    # Calls:   auth_service.blacklist_token()
    # Returns: 200
    pass


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    # Purpose: Send password reset email/OTP
    # Input:   { email }
    # Calls:   auth_service.send_reset_token()
    # Returns: 200 (always, prevents email enumeration)
    pass


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    # Purpose: Set new password with reset token
    # Input:   { reset_token, new_password }
    # Calls:   auth_service.reset_password()
    # Returns: 200 or 400/401
    pass
