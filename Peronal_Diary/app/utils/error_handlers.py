"""
Error Handlers — global exception handlers registered in app factory.

Error Codes:
  VALIDATION_ERROR    → 400
  UNAUTHORIZED        → 401
  FORBIDDEN           → 403
  NOT_FOUND           → 404
  CONFLICT            → 409 (e.g., duplicate email)
  RATE_LIMITED        → 429
  NLP_FAILURE         → 422 (ask user to rephrase)
  INTERNAL_ERROR      → 500
  DB_ERROR            → 500 (rollback applied)
"""


class AppError(Exception):
    """Base application error with status code and error code."""

    def __init__(self, message, status_code=400, code=None):
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(self.message)


class ValidationError(AppError):
    def __init__(self, message='Validation failed', errors=None):
        super().__init__(message, 400, 'VALIDATION_ERROR')
        self.errors = errors


class NotFoundError(AppError):
    def __init__(self, resource='Resource'):
        super().__init__(f'{resource} not found', 404, 'NOT_FOUND')


class ConflictError(AppError):
    def __init__(self, message='Resource already exists'):
        super().__init__(message, 409, 'CONFLICT')


class NLPFailureError(AppError):
    def __init__(self, message='Could not understand input, please rephrase'):
        super().__init__(message, 422, 'NLP_FAILURE')


def register_error_handlers(app):
    # Register AppError handler → return JSON error response
    # Register SQLAlchemy IntegrityError → 409 CONFLICT
    # Register generic Exception → 500 INTERNAL_ERROR with rollback
    pass
