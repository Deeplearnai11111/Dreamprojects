from app import db


class Plan(db.Model):

    __tablename__ = 'plans'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ====================================
    # RELATION WITH FREQUENCY
    # ====================================

    frequency_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'frequencies.id',
            ondelete='CASCADE'
        ),
        nullable=False
    )

    # ====================================
    # BASIC DETAILS
    # ====================================

    name = db.Column(
        db.String(100),
        nullable=False
    )

    subtitle = db.Column(
        db.String(200)
    )

    description = db.Column(
        db.Text
    )

    price = db.Column(
        db.Integer,
        nullable=False
    )

    badge = db.Column(
        db.String(100)
    )

    # ====================================
    # UI THEME
    # ====================================

    theme = db.Column(
        db.String(50),
        default='blue'
    )

    # ====================================
    # SERVICE FEATURES
    # ====================================

    exterior_wash = db.Column(
        db.Boolean,
        default=True
    )

    interior_cleaning = db.Column(
        db.Boolean,
        default=False
    )

    tyre_rinse = db.Column(
        db.Boolean,
        default=False
    )

    tyre_dressing = db.Column(
        db.Boolean,
        default=False
    )

    dashboard_polish = db.Column(
        db.Boolean,
        default=False
    )

    vacuum_cleaning = db.Column(
        db.Boolean,
        default=False
    )

    perfume_finish = db.Column(
        db.Boolean,
        default=False
    )

    # ====================================
    # PLAN STATUS
    # ====================================

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    is_popular = db.Column(
        db.Boolean,
        default=False
    )

    # ====================================
    # ANALYTICS
    # ====================================

    total_subscribers = db.Column(
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
    # RELATIONSHIPS
    # ====================================

    frequency = db.relationship(
        'Frequency',
        backref='frequency_plans'
    )

    slots = db.relationship(
        'Slot',
        cascade='all, delete-orphan',
        lazy=True
    )

    # ====================================
    # STRING REPRESENTATION
    # ====================================

    def __repr__(self):

        return f'<Plan {self.name}>'