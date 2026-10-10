"""
Rate Limiter — per-user, per-endpoint throttling.
Uses Flask-Limiter with Redis backend.

Limits:
  Auth endpoints:       5 requests/minute (brute force prevention)
  Voice/Upload:         30 requests/hour (resource-intensive)
  Query endpoints:      60 requests/hour
  Standard CRUD:        120 requests/minute

On limit exceeded: return 429 Too Many Requests
"""


def init_rate_limiter(app):
    # Initialize Flask-Limiter with Redis storage
    # Set default limits
    # Return limiter instance
    pass
