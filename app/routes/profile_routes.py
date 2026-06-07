from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required
from flask_login import current_user

from werkzeug.utils import secure_filename

from app import db

from app.models.car import Car
from app.models.booking import Booking
from app.models.service_update import ServiceUpdate
from app.models.payment import Payment
from app.models.car import Car as CarModel

import os


profile = Blueprint(
    'profile',
    __name__
)


# ====================================
# PROFILE PAGE
# ====================================

@profile.route('/profile')
@login_required
def profile_page():

    # ====================================
    # USER CARS
    # ====================================

    cars = Car.query.filter_by(
        user_id=current_user.id
    ).all()

    # ====================================
    # BOOKINGS
    # ====================================

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Booking.id.desc()
    ).all()

    latest_booking = None

    if bookings:

        latest_booking = bookings[0]

    # ====================================
    # SERVICE UPDATES
    # ====================================

    service_updates = []

    if latest_booking:

        service_updates = ServiceUpdate.query.filter_by(

            booking_id=latest_booking.id

        ).order_by(

            ServiceUpdate.id.desc()

        ).all()

    # ====================================
    # STATS
    # ====================================

    total_cars = len(cars)

    total_bookings = len(bookings)

    completed_services = Booking.query.filter_by(

        user_id=current_user.id,

        is_completed=True

    ).count()

    active_services = Booking.query.filter_by(

        user_id=current_user.id,

        is_completed=False

    ).count()

    # ====================================
    # LIVE STATUS
    # ====================================

    live_status = 'No Active Service'

    progress_percentage = 0

    current_stage = 'Waiting'

    estimated_delivery = 'Updating Soon'

    current_work = 'No active work'

    next_step = 'Waiting for booking'

    pickup_message = None

    if latest_booking:

        live_status = (

            latest_booking.service_status
            or 'Scheduled'

        )

        progress_percentage = (

            latest_booking.progress_percentage
            or 0

        )

        current_stage = (

            latest_booking.service_stage
            or 'Booking Confirmed'

        )

        estimated_delivery = (

            latest_booking.estimated_delivery
            or 'Updating Soon'

        )

        current_work = (

            latest_booking.current_work
            or 'Work update pending'

        )

        next_step = (

            latest_booking.next_step
            or 'Next update soon'

        )

        if latest_booking.pickup_ready:

            pickup_message = (

                latest_booking.pickup_message
                or
                'Vehicle Ready For Pickup'
            )

    # ====================================
    # SERVICE COLOR
    # ====================================

    if progress_percentage >= 100:

        service_color = '#4dff88'

    elif progress_percentage >= 60:

        service_color = '#39cfff'

    else:

        service_color = '#ffb347'

    # ====================================
    # RECENT ACTIVITY
    # ====================================

    recent_activity = []

    for update in service_updates[:5]:

        recent_activity.append({

            'title':
            update.stage,

            'message':
            update.description,

            'time':
            update.created_at.strftime(
                '%d %b %Y | %I:%M %p'
            ),

            'progress':
            update.progress
        })

    # ====================================
    # PAGE
    # ====================================
    # ====================================
    # PAYMENTS
    # ====================================

    payments = Payment.query.join(

        Booking,

        Payment.booking_id == Booking.id

    ).filter(

        Booking.user_id == current_user.id

    ).order_by(

        Payment.id.desc()

    ).all()

    return render_template(

        'profile/profile.html',

        user=current_user,

        cars=cars,

        bookings=bookings,

        booking=latest_booking,

        service_updates=service_updates,

        total_cars=total_cars,

        total_bookings=total_bookings,

        completed_services=completed_services,

        active_services=active_services,

        live_status=live_status,

        progress_percentage=progress_percentage,

        current_stage=current_stage,

        estimated_delivery=estimated_delivery,

        current_work=current_work,

        next_step=next_step,

        pickup_message=pickup_message,

        service_color=service_color,

        recent_activity=recent_activity
        ,
        payments=payments
    )


# ====================================
# STATIC POLICY PAGES
# ====================================


@profile.route('/privacy')
def privacy_page():
    return render_template('privacy.html')


@profile.route('/terms')
def terms_page():
    return render_template('terms.html')



# API: get car details (JSON)
@profile.route('/api/car/<int:car_id>')
@login_required
def api_get_car(car_id):

    car = CarModel.query.filter_by(id=car_id, user_id=current_user.id).first()

    if not car:
        return ({'error': 'Car not found'}, 404)

    return ({
        'id': car.id,
        'registration_number': car.registration_number,
        'car_model': car.car_model,
        'car_brand': car.car_brand,
        'car_colour': car.car_colour
    }, 200)


# UPDATE CAR
@profile.route('/update-car/<int:car_id>', methods=['POST'])
@login_required
def update_car(car_id):

    car = CarModel.query.filter_by(id=car_id, user_id=current_user.id).first()

    if not car:
        flash('Car not found')
        return redirect(url_for('profile.profile_page'))

    registration_number = request.form.get('registration_number')
    car_model = request.form.get('car_model')
    car_brand = request.form.get('car_brand')
    car_colour = request.form.get('car_colour')

    if registration_number:
        car.registration_number = registration_number

    car.car_model = car_model
    car.car_brand = car_brand
    car.car_colour = car_colour

    db.session.commit()

    flash('Car updated')
    return redirect(url_for('profile.profile_page'))


# ====================================
# ADD CAR
# ====================================

@profile.route(
    '/add-car',
    methods=['POST']
)
@login_required
def add_car():

    registration_number = request.form.get(
        'registration_number'
    )

    car_model = request.form.get(
        'car_model'
    )

    car_brand = request.form.get(
        'car_brand'
    )

    car_colour = request.form.get(
        'car_colour'
    )

    if not registration_number:

        flash(
            'Enter Registration Number'
        )

        return redirect(
            url_for(
                'profile.profile_page'
            )
        )

    new_car = Car(

        user_id=current_user.id,

        registration_number=registration_number,

        car_model=car_model,

        car_brand=car_brand,

        car_colour=car_colour
    )

    db.session.add(
        new_car
    )

    db.session.commit()

    flash(
        'Car Added Successfully'
    )

    return redirect(
        url_for(
            'profile.profile_page'
        )
    )


# ====================================
# DELETE CAR
# ====================================

@profile.route(
    '/delete-car/<int:car_id>'
)
@login_required
def delete_car(car_id):

    car = Car.query.filter_by(

        id=car_id,

        user_id=current_user.id

    ).first()

    if not car:

        flash(
            'Car Not Found'
        )

        return redirect(
            url_for(
                'profile.profile_page'
            )
        )

    db.session.delete(
        car
    )

    db.session.commit()

    flash(
        'Car Removed'
    )

    return redirect(
        url_for(
            'profile.profile_page'
        )
    )


# ====================================
# UPLOAD PROFILE IMAGE
# ====================================

@profile.route(
    '/upload-profile-image',
    methods=['POST']
)
@login_required
def upload_profile_image():

    if 'profile_image' not in request.files:

        flash(
            'No Image Selected'
        )

        return redirect(
            url_for(
                'profile.profile_page'
            )
        )

    image = request.files.get(
        'profile_image'
    )

    if image.filename == '':

        flash(
            'Select Image'
        )

        return redirect(
            url_for(
                'profile.profile_page'
            )
        )

    filename = secure_filename(
        image.filename
    )

    filename = (
        str(current_user.id)
        + '_'
        + filename
    )

    upload_folder = os.path.join(

        'app',
        'static',
        'uploads',
        'profile_pics'
    )

    os.makedirs(

        upload_folder,

        exist_ok=True
    )

    image_path = os.path.join(

        upload_folder,

        filename
    )

    image.save(
        image_path
    )

    # DELETE OLD IMAGE

    if (
        current_user.profile_image
        and
        current_user.profile_image != 'default.png'
    ):

        old_path = os.path.join(

            upload_folder,

            current_user.profile_image
        )

        if os.path.exists(old_path):

            os.remove(old_path)

    current_user.profile_image = filename

    db.session.commit()

    flash(
        'Profile Updated'
    )

    return redirect(
        url_for(
            'profile.profile_page'
        )
    )


# ====================================
# UPDATE PROFILE
# ====================================


@profile.route(
    '/update-profile',
    methods=['POST']
)
@login_required
def update_profile():

    full_name = request.form.get('full_name')

    phone = request.form.get('phone')

    society = request.form.get('society')

    block = request.form.get('block')

    flat_number = request.form.get('flat_number')

    if full_name:

        current_user.full_name = full_name

    if phone:

        current_user.phone = phone

    current_user.society = society

    current_user.block = block

    current_user.flat_number = flat_number

    db.session.commit()

    flash('Profile updated')

    return redirect(url_for('profile.profile_page'))


# ====================================
# DELETE PROFILE IMAGE
# ====================================

@profile.route(
    '/delete-profile-image'
)
@login_required
def delete_profile_image():

    upload_folder = os.path.join(

        'app',
        'static',
        'uploads',
        'profile_pics'
    )

    if (
        current_user.profile_image
        and
        current_user.profile_image != 'default.png'
    ):

        old_path = os.path.join(

            upload_folder,

            current_user.profile_image
        )

        if os.path.exists(old_path):

            os.remove(old_path)

    current_user.profile_image = 'default.png'

    db.session.commit()

    flash(
        'Profile Image Removed'
    )

    return redirect(
        url_for(
            'profile.profile_page'
        )
    )