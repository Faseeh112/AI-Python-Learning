"""
Flask Application Factory
Creates and configures the Flask app instance.
"""
import os
from flask import Flask
from config.settings import config_by_name
from app.extensions import db, migrate, jwt, cors, ma


def create_app(config_name=None):
    """Create Flask application."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    ma.init_app(app)

    # Register blueprints
    _register_blueprints(app)

    # Register error handlers
    _register_error_handlers(app)

    # Create upload folder
    os.makedirs(app.config.get('UPLOAD_FOLDER', './uploads'), exist_ok=True)

    return app


def _register_blueprints(app):
    """Register all route blueprints."""
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.notes_routes import notes_bp
    from app.routes.voice_routes import voice_bp
    from app.routes.transaction_routes import transaction_bp
    from app.routes.asset_routes import asset_bp
    from app.routes.person_routes import person_bp
    from app.routes.location_routes import location_bp
    from app.routes.event_routes import event_bp
    from app.routes.reminder_routes import reminder_bp
    from app.routes.document_routes import document_bp
    from app.routes.upload_routes import upload_bp
    from app.routes.category_routes import category_bp
    from app.routes.tag_routes import tag_bp
    from app.routes.quran_routes import quran_bp
    from app.routes.knowledge_routes import knowledge_bp
    from app.routes.query_routes import query_bp
    from app.routes.zakat_routes import zakat_bp
    from app.routes.tax_routes import tax_bp

    blueprints = [
        auth_bp, user_bp, notes_bp, voice_bp, transaction_bp,
        asset_bp, person_bp, location_bp, event_bp, reminder_bp,
        document_bp, upload_bp, category_bp, tag_bp, quran_bp,
        knowledge_bp, query_bp, zakat_bp, tax_bp,
    ]

    for bp in blueprints:
        app.register_blueprint(bp)


def _register_error_handlers(app):
    """Register global error handlers."""
    from app.utils.response_helpers import error_response

    @app.errorhandler(400)
    def bad_request(e):
        return error_response('Bad request', 400)

    @app.errorhandler(401)
    def unauthorized(e):
        return error_response('Unauthorized', 401)

    @app.errorhandler(403)
    def forbidden(e):
        return error_response('Forbidden', 403)

    @app.errorhandler(404)
    def not_found(e):
        return error_response('Resource not found', 404)

    @app.errorhandler(429)
    def rate_limited(e):
        return error_response('Too many requests', 429)

    @app.errorhandler(500)
    def server_error(e):
        return error_response('Internal server error', 500)
