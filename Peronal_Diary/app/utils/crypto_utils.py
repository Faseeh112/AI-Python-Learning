"""
Crypto Utilities — password hashing and token helpers.
Uses bcrypt for password hashing.
"""


def hash_password(plain_password):
    # Hash password using bcrypt
    # Return bytes for VARBINARY(256) storage
    pass


def verify_password(plain_password, password_hash):
    # Verify plain password against stored bcrypt hash
    # Return True/False
    pass


def generate_reset_token(user_id, expires_minutes=30):
    # Generate time-limited password reset token
    # Encode user_id + expiry into JWT or random token
    # Return token string
    pass


def verify_reset_token(token):
    # Decode and validate reset token
    # Check expiry
    # Return user_id or None
    pass
