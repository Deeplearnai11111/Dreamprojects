from app import db

from datetime import datetime


class Booking(db.Model):

    __tablename__ = 'bookings'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ====================================
    # USER
    # ====================================

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    # ====================================
    # PLAN
    # ====================================

    plan_name = db.Column(
        db.String(100)
    )

    plan_price = db.Column(
        db.Integer,
        default=0
    )

    # ====================================
    # SLOT
    # ====================================

    slot_id = db.Column(
        db.Integer
    )

    service_time = db.Column(
        db.String(100)
    )

    frequency = db.Column(
        db.String(100)
    )

    # ====================================
    # PAYMENT
    # ====================================

    payment_status = db.Column(
        db.String(50),
        default='Pending'
    )

    payment_method = db.Column(
        db.String(100)
    )

    transaction_id = db.Column(
        db.String(200)
    )

    is_payment_completed = db.Column(
        db.Boolean,
        default=False
    )

    # ====================================
    # SERVICE STATUS
    # ====================================

    booking_status = db.Column(
        db.String(100),
        default='Pending'
    )

    service_status = db.Column(
        db.String(100),
        default='Scheduled'
    )

    service_stage = db.Column(
        db.String(100),
        default='Booking Confirmed'
    )

    progress_percentage = db.Column(
        db.Integer,
        default=0
    )

    is_completed = db.Column(
        db.Boolean,
        default=False
    )

    pickup_ready = db.Column(
        db.Boolean,
        default=False
    )

    # ====================================
    # LIVE TRACKING
    # ====================================

    garage_status = db.Column(
        db.String(200)
    )

    service_note = db.Column(
        db.Text
    )

    current_work = db.Column(
        db.Text
    )

    completed_work = db.Column(
        db.Text
    )

    pending_work = db.Column(
        db.Text
    )

    next_step = db.Column(
        db.Text
    )

    estimated_delivery = db.Column(
        db.String(100)
    )

    # ====================================
    # NOTIFICATION
    # ====================================

    latest_notification = db.Column(
        db.Text
    )

    notification_time = db.Column(
        db.String(100)
    )

    unread_notification = db.Column(
        db.Boolean,
        default=False
    )

    # ====================================
    # PICKUP
    # ====================================

    pickup_message = db.Column(
        db.Text
    )

    completion_message = db.Column(
        db.Text
    )

    # ====================================
    # SERVICE TYPE
    # ====================================

    service_category = db.Column(
        db.String(100),
        default='Car Wash'
    )

    # ====================================
    # CREATED
    # ====================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ====================================
    # UPDATE PROGRESS
    # ====================================

    def update_progress(self):

        if self.progress_percentage >= 100:

            self.is_completed = True

            self.pickup_ready = True

            self.service_status = 'Completed'

    # ====================================
    # STRING
    # ====================================

    def __repr__(self):

        return f'<Booking {self.id}>'
    
    service_stage = db.Column(
    db.String(30),
    default='Assigned'
)

rating_submitted = db.Column(
    db.Boolean,
    default=False
)

rating = db.Column(
    db.Integer
)

review = db.Column(
    db.Text
)