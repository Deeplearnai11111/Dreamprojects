from app import db

from flask_login import UserMixin

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from datetime import datetime


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True
    )

    phone = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    society = db.Column(
        db.String(120)
    )

    block = db.Column(
        db.String(50)
    )

    flat_number = db.Column(
        db.String(50)
    )

    profile_image = db.Column(
        db.String(255),
        default='default.png'
    )

    active_plan = db.Column(
        db.String(100),
        default='No Active Plan'
    )

    account_status = db.Column(
        db.String(50),
        default='Active'
    )

    customer_type = db.Column(
        db.String(50),
        default='Regular'
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    # ====================================
    # ROLE
    # user
    # admin
    # super_admin
    # ====================================

    role = db.Column(
        db.String(20),
        nullable=False,
        default='user'
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # session token used to invalidate other sessions when user logs out
    session_token = db.Column(
        db.String(64),
        nullable=True
    )

    # ====================================
    # PASSWORD HASH
    # ====================================

    def set_password(self, raw_password):

        self.password = generate_password_hash(
            raw_password
        )

    def check_password(self, raw_password):

        return check_password_hash(
            self.password,
            raw_password
        )

    def __repr__(self):

        return f'<User {self.full_name}>'
    
    