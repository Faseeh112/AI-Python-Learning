"""
Standard API response format helpers.
"""
from flask import jsonify


def success_response(data=None, message='Success', status_code=200, meta=None):
    """Return a standardized success response."""
    response = {
        'status': 'success',
        'message': message,
        'data': data,
    }
    if meta:
        response['meta'] = meta
    return jsonify(response), status_code


def error_response(message='Error', status_code=400, errors=None, code=None):
    """Return a standardized error response."""
    response = {
        'status': 'error',
        'message': message,
    }
    if errors:
        response['errors'] = errors
    if code:
        response['code'] = code
    return jsonify(response), status_code


def paginated_response(data, page, per_page, total):
    """Return a paginated success response."""
    return success_response(
        data=data,
        meta={
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': (total + per_page - 1) // per_page,
        }
    )
