import os

class Config:

    SECRET_KEY = 'goclean_super_secret_key'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///goclean.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Google OAuth (set via environment variables in production)
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')

    # Email settings for password reset OTP
    MAIL_SERVER = os.environ.get('MAIL_SERVER', '')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ('true', '1', 'yes')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() in ('true', '1', 'yes')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME or 'noreply@cleanzo.in')