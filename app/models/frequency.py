from app import db


class Frequency(db.Model):

    __tablename__ = 'frequencies'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ====================================
    # BASIC DETAILS
    # ====================================

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    subtitle = db.Column(
        db.String(200)
    )

    washes_per_month = db.Column(
        db.Integer,
        default=0
    )

    # ====================================
    # UI SETTINGS
    # ====================================

    theme_color = db.Column(
        db.String(50),
        default='#39cfff'
    )

    icon = db.Column(
        db.String(100),
        default='calendar'
    )

    # ====================================
    # DISPLAY CONTROL
    # ====================================

    display_order = db.Column(
        db.Integer,
        default=1
    )

    is_popular = db.Column(
        db.Boolean,
        default=False
    )

    is_recommended = db.Column(
        db.Boolean,
        default=False
    )

    # ====================================
    # STATUS
    # ====================================

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    # ====================================
    # ANALYTICS
    # ====================================

    total_users = db.Column(
        db.Integer,
        default=0
    )

    # ====================================
    # TIMESTAMP
    # ====================================

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # ====================================
    # RELATIONSHIP
    # ====================================

    plans = db.relationship(
        'Plan',
        cascade='all, delete-orphan',
        lazy=True
    )

    # ====================================
    # STRING
    # ====================================

    def __repr__(self):

        return f'<Frequency {self.name}>'