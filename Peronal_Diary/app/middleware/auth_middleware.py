"""
Auth Middleware — JWT verification and token management.
Uses Flask-JWT-Extended.

Access Token:  short-lived (15 min), in Authorization: Bearer header
Refresh Token: long-lived (7 days), httpOnly cookie (web) or secure storage (mobile)
Token Blacklist: on logout, add JTI to Redis/DB blacklist
"""
from functools import wraps


def jwt_required_custom():
    # Decorator: verify JWT access token
    # Extract user_id from token claims
    # Check token not blacklisted
    # Inject current_user into request context
    pass


def refresh_token_required():
    # Decorator: verify JWT refresh token
    # Used only on /api/auth/refresh endpoint
    pass


def get_current_user_id():
    # Extract user_id from current JWT claims
    # Return user_id or raise 401
    pass
