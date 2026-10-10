"""
Test Fixtures — shared setup for all test modules.
"""
# import pytest
# from app import create_app
# from app.extensions import db as _db


# @pytest.fixture(scope='session')
# def app():
#     """Create Flask app with testing config."""
#     app = create_app('testing')
#     with app.app_context():
#         _db.create_all()
#         yield app
#         _db.drop_all()


# @pytest.fixture(scope='function')
# def db_session(app):
#     """Provide a clean DB session per test (rollback after each)."""
#     with app.app_context():
#         connection = _db.engine.connect()
#         transaction = connection.begin()
#         session = _db.create_scoped_session(
#             options={'bind': connection, 'binds': {}}
#         )
#         _db.session = session
#         yield session
#         transaction.rollback()
#         connection.close()
#         session.remove()


# @pytest.fixture
# def client(app):
#     """Flask test client."""
#     return app.test_client()


# @pytest.fixture
# def auth_headers(client):
#     """Register + login a test user, return JWT auth headers."""
#     # POST /api/auth/register with test user
#     # POST /api/auth/login
#     # Extract access_token
#     # Return { 'Authorization': 'Bearer <token>' }
#     pass
