"""
Input Validators — reusable validation helpers.
"""
import re


def validate_email(email):
    # Validate email format using regex
    # Return True/False
    pass


def validate_password_strength(password):
    # Check: min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char
    # Return { valid: bool, errors: [] }
    pass


def validate_currency_code(code):
    # Check code is 3 uppercase letters and exists in currency table
    # Return True/False
    pass


def validate_file_extension(filename, allowed_extensions):
    # Check file extension against whitelist
    # Return True/False
    pass


def validate_date_range(date_from, date_to):
    # Ensure date_from <= date_to
    # Parse date strings to date objects
    # Return (date_from, date_to) or raise validation error
    pass
