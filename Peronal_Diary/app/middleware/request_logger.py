"""
Request Logger — audit logging for all API requests.

Logs: timestamp, method, path, user_id, response_status, duration_ms
Excludes: health check, static files
Redacts: password, token fields
"""


def init_request_logger(app):
    # Register before_request and after_request hooks
    # Log request/response metadata
    # Redact sensitive fields
    pass
