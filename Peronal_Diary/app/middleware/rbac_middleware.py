"""
RBAC Middleware — Role-Based Access Control + Ownership verification.

Roles (future expansion):
  'user'  — standard access to own data
  'admin' — category management, system views

Every data endpoint must verify user_id matches JWT user.
"""
from functools import wraps


def require_ownership(model_class, id_param_name):
    # Decorator: fetches record by id_param_name
    # Checks record.user_id == current JWT user_id
    # Returns 403 if mismatch, 404 if not found
    # Injects fetched record into kwargs
    pass


def admin_required():
    # Decorator: checks current user has admin role
    # Returns 403 if not admin
    pass
