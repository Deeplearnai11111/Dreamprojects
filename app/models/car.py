from app import db


class Car(db.Model):

    __tablename__ = 'cars'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    registration_number = db.Column(
        db.String(100),
        nullable=False
    )

    car_brand = db.Column(
        db.String(100)
    )

    car_model = db.Column(
        db.String(100)
    )

    car_colour = db.Column(
        db.String(100)
    )

    fuel_type = db.Column(
        db.String(50),
        default='Petrol'
    )

    transmission = db.Column(
        db.String(50),
        default='Manual'
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):

        return f'<Car {self.registration_number}>'