from app import db


class Slot(db.Model):

    __tablename__ = 'slots'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ====================================
    # RELATIONS
    # ====================================

    frequency_id = db.Column(
        db.Integer,
        db.ForeignKey('frequencies.id'),
        nullable=False
    )

    plan_id = db.Column(
        db.Integer,
        db.ForeignKey('plans.id'),
        nullable=False
    )

    # ====================================
    # SLOT DETAILS
    # ====================================

    slot_time = db.Column(
        db.String(50),
        nullable=False
    )

    shift = db.Column(
        db.String(50)
    )
    # Morning / Afternoon / Evening

    slot_type = db.Column(
        db.String(50)
    )
    # Standard / Express / Premium etc

    slot_label = db.Column(
        db.String(100)
    )
    # Prime Morning Slot etc

    # ====================================
    # BOOKING CONTROL
    # ====================================

    max_bookings = db.Column(
        db.Integer,
        default=10
    )

    current_bookings = db.Column(
        db.Integer,
        default=0
    )

    remaining_slots = db.Column(
        db.Integer,
        default=10
    )

    # ====================================
    # SLOT STATUS
    # ====================================

    status = db.Column(
        db.String(50),
        default='Open'
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    is_full = db.Column(
        db.Boolean,
        default=False
    )

    is_priority = db.Column(
        db.Boolean,
        default=False
    )

    is_recommended = db.Column(
        db.Boolean,
        default=False
    )

    # ====================================
    # UI
    # ====================================

    slot_color = db.Column(
        db.String(50),
        default='#39cfff'
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
        backref='slots'
    )

    plan = db.relationship(
    'Plan'
)

    # ====================================
    # AUTO SLOT STATUS
    # ====================================

    def update_slot_status(self):

        self.remaining_slots = (
            self.max_bookings -
            self.current_bookings
        )

        if (
            self.current_bookings >=
            self.max_bookings
        ):

            self.is_full = True

            self.status = 'Full'

        else:

            self.is_full = False

            self.status = 'Open'

    # ====================================
    # STRING
    # ====================================

    def __repr__(self):

        return (
            f'<Slot '
            f'{self.slot_time} | '
            f'{self.shift}>'
        )