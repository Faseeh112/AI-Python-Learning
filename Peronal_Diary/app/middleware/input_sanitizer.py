"""
Input Sanitizer — XSS/injection prevention.

Uses marshmallow/pydantic schemas for input validation.
Each endpoint defines a schema with:
  - Required vs optional fields
  - Type validation
  - Length constraints matching DB schema
  - Enum validation (direction, note_type, purpose, etc.)
  - Amount >= 0 checks
  - Date format validation
"""
from functools import wraps


def validate_input(schema_class):
    # Decorator: validates request JSON against marshmallow schema
    # On validation failure: return 400 with field-level errors
    # On success: inject validated data into kwargs
    pass


def sanitize_string(text):
    # Strip HTML tags, escape special characters
    # Prevent XSS in stored text fields
    # Return sanitized string
    pass
