from app import db


class Payment(db.Model):

    __tablename__ = 'payments'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    booking_id = db.Column(
        db.Integer,
        db.ForeignKey('bookings.id')
    )

    amount = db.Column(
        db.Integer,
        nullable=False
    )

    payment_method = db.Column(
        db.String(50)
    )

    transaction_id = db.Column(
        db.String(150)
    )

    payment_status = db.Column(
        db.String(50),
        default='Pending'
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )