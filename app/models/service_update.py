from app import db


class ServiceUpdate(db.Model):

    __tablename__ = 'service_updates'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    booking_id = db.Column(
        db.Integer,
        db.ForeignKey('bookings.id')
    )

    stage = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.Text
    )

    progress = db.Column(
        db.Integer,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )