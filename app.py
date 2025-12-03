from flask import Flask, g, session, request
import flask
from config import Config
from models import db, User
from routes.main import main_bp
from routes.auth import auth_bp
from routes.quests import quests_bp
from routes.admin import admin_bp
from routes.rewards import rewards_bp
from routes.onboarding import onboarding_bp
from routes.profile import profile_bp
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import secrets

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Simple CSRF implementation (avoid external Flask-WTF compatibility issues)
    # We store a per-session random value and generate a timed token for templates.
    csrf_serializer = URLSafeTimedSerializer(app.config.get('SECRET_KEY', 'csrf-secret'), salt='csrf-token')

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(quests_bp, url_prefix='/quests')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(rewards_bp, url_prefix='/rewards')
    app.register_blueprint(onboarding_bp, url_prefix='/onboarding')
    app.register_blueprint(profile_bp, url_prefix='/profile')

    @app.before_request
    def load_logged_in_user():
        """Attach the logged-in user to flask.g for easy template access."""
        user_id = session.get('user_id')
        g.user = User.query.get(user_id) if user_id else None

    @app.context_processor
    def inject_current_user():
        return {'current_user': getattr(g, 'user', None)}


    @app.context_processor
    def inject_csrf_token():
        def _gen():
            if 'csrf_token' not in session:
                session['csrf_token'] = secrets.token_urlsafe(16)
            return csrf_serializer.dumps(session['csrf_token'])
        return {'csrf_token': _gen}

    @app.before_request
    def _validate_csrf():
        # Validate CSRF on state-changing methods
        if flask.request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            # Allow certain admin public endpoints to handle their own checks
            token = flask.request.form.get('csrf_token') or flask.request.headers.get('X-CSRFToken')
            if not token:
                return 'Missing CSRF token', 400
            try:
                val = csrf_serializer.loads(token, max_age=3600)
            except (BadSignature, SignatureExpired):
                return 'Invalid CSRF token', 400
            if session.get('csrf_token') != val:
                return 'Invalid CSRF token', 400

    with app.app_context():
        # In production, use migrations. For dev/prototype, create all.
        # db.create_all() 
        pass

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
