from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

import os
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv


# ====================================
# EXTENSIONS
# ====================================

db = SQLAlchemy()

login_manager = LoginManager()

migrate = Migrate()

# OAuth
oauth = OAuth()

# Load .env (support both KEY=VALUE and Windows 'set KEY=VALUE' lines)
def _load_project_env():
    # project root is one level up from app/
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_path = os.path.join(project_root, '.env')
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for raw in f:
                    line = raw.strip()
                    if not line or line.startswith('#'):
                        continue
                    # support lines like: set KEY=VALUE
                    if line.lower().startswith('set '):
                        kv = line[4:]
                        if '=' in kv:
                            k, v = kv.split('=', 1)
                            if k and v:
                                os.environ.setdefault(k.strip(), v.strip().strip('"\''))
        except Exception:
            pass
        # let python-dotenv handle standard KEY=VALUE lines
        try:
            load_dotenv(env_path)
        except Exception:
            pass


# load env early
_load_project_env()


# ====================================
# LOGIN CONFIG
# ====================================

login_manager.login_view = 'auth.login'

login_manager.login_message = None


# ====================================
# CREATE APP
# ====================================

def create_app():

    app = Flask(__name__)

    # ====================================
    # CONFIG
    # ====================================

    app.config.from_object(
        'config.Config'
    )

    # ====================================
    # INIT EXTENSIONS
    # ====================================

    db.init_app(app)

    login_manager.init_app(app)

    migrate.init_app(app, db)
    oauth.init_app(app)

    # register google oauth client using config
    try:
        oauth.register(
            name='google',
            client_id=app.config.get('GOOGLE_CLIENT_ID'),
            client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
            access_token_url='https://oauth2.googleapis.com/token',
            authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
            api_base_url='https://www.googleapis.com/oauth2/v2/',
            # use OpenID Connect discovery metadata so Authlib can find jwks_uri
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={'scope': 'openid email profile'}
        )
    except Exception:
        # ignore registration errors at startup if config missing
        pass

    # ====================================
    # LOGIN SETTINGS
    # ====================================

    login_manager.login_view = 'auth.login'

    login_manager.login_message = (
        'Please login first'
    )

    # ====================================
    # CREATE UPLOAD FOLDERS
    # ====================================

    os.makedirs(
        'app/static/uploads/profile_pics',
        exist_ok=True
    )

    os.makedirs(
        'app/static/uploads/service_updates',
        exist_ok=True
    )

    os.makedirs(
        'app/static/uploads/payment_screenshots',
        exist_ok=True
    )

    # ====================================
    # IMPORT MODELS
    # ====================================

    from app.models.user import User

    from app.models.car import Car

    from app.models.booking import Booking

    from app.models.payment import Payment

    from app.models.frequency import Frequency

    from app.models.plan import Plan

    from app.models.slot import Slot

    from app.models.service_update import (
        ServiceUpdate
    )

    # ====================================
    # USER LOADER
    # ====================================

    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(
            int(user_id)
        )

    # ====================================
    # IMPORT ROUTES
    # ====================================

    from app.routes.auth_routes import auth

    from app.routes.booking_routes import booking

    from app.routes.payment_routes import payment

    from app.routes.tracking_routes import tracking

    from app.routes.profile_routes import profile

    from app.routes.plan_routes import plans

    from app.routes.admin_routes import admin

    # ====================================
    # REGISTER BLUEPRINTS
    # ====================================

    app.register_blueprint(auth)

    app.register_blueprint(booking)

    app.register_blueprint(payment)

    app.register_blueprint(tracking)

    app.register_blueprint(profile)

    app.register_blueprint(plans)

    app.register_blueprint(admin)

    # ====================================
    # GLOBAL SESSION TOKEN CHECK
    # Invalidate sessions when a user's session_token doesn't match the one stored in Flask session
    from flask import session, redirect, url_for, flash
    from flask_login import logout_user, current_user

    @app.before_request
    def check_session_token():
        try:
            if current_user and current_user.is_authenticated:
                token = session.get('session_token')
                # if user's token is missing or differs, force logout
                if not getattr(current_user, 'session_token', None) or token != current_user.session_token:
                    session.pop('session_token', None)
                    logout_user()
                    flash('You have been logged out.')
                    return redirect(url_for('auth.login'))
        except Exception:
            # on any error, allow request to continue (avoid locking out admins during startup)
            return None

    # ====================================
    # CREATE DATABASE TABLES
    # ====================================

    with app.app_context():

        db.create_all()

    # ====================================
    # RETURN APP
    # ====================================

    return app