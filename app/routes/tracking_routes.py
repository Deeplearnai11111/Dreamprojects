from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required
from flask_login import current_user

from app.models.booking import Booking
from app.models.service_update import ServiceUpdate


tracking = Blueprint(
    'tracking',
    __name__
)


# ====================================
# TRACKING PAGE
# ====================================

@tracking.route('/tracking')
@login_required
def tracking_page():

    # ====================================
    # GET LATEST BOOKING
    # ====================================

    latest_booking = Booking.query.filter_by(

        user_id=current_user.id

    ).order_by(

        Booking.id.desc()

    ).first()

    # ====================================
    # NO BOOKING
    # ====================================

    if not latest_booking:

        flash(
            'No Active Booking Found'
        )

        return redirect(
            url_for(
                'plans.plans_page'
            )
        )

    # ====================================
    # SERVICE UPDATES
    # ====================================

    service_updates = ServiceUpdate.query.filter_by(

        booking_id=latest_booking.id

    ).order_by(

        ServiceUpdate.id.desc()

    ).all()

    # ====================================
    # PROGRESS
    # ====================================

    progress_percentage = (

        latest_booking.progress_percentage
        or 0

    )

    # ====================================
    # TIMELINE
    # ====================================

    tracking_steps = [

        {
            'title':
            'Booking Confirmed',

            'status':
            'completed'
            if progress_percentage >= 10
            else 'pending',

            'message':
            'Booking successfully confirmed.'
        },

        {
            'title':
            'Vehicle Received',

            'status':
            'completed'
            if progress_percentage >= 25
            else 'pending',

            'message':
            'Vehicle received by CLEANZO.'
        },

        {
            'title':
            'Inspection Started',

            'status':
            'completed'
            if progress_percentage >= 40
            else 'pending',

            'message':
            'Initial inspection running.'
        },

        {
            'title':
            'Service Started',

            'status':
            'completed'
            if progress_percentage >= 55
            else 'pending',

            'message':
            'Cleaning work started.'
        },

        {
            'title':
            'Work In Progress',

            'status':
            'completed'
            if progress_percentage >= 75
            else 'pending',

            'message':
            latest_booking.service_note
            or
            'Team currently working.'
        },

        {
            'title':
            'Quality Check',

            'status':
            'completed'
            if progress_percentage >= 90
            else 'pending',

            'message':
            'Final quality inspection.'
        },

        {
            'title':
            'Ready For Pickup',

            'status':
            'completed'
            if latest_booking.pickup_ready
            else 'pending',

            'message':
            latest_booking.completion_message
            or
            'Vehicle ready for pickup.'
        }

    ]

    # ====================================
    # CURRENT STATUS
    # ====================================

    current_stage = (

        latest_booking.service_stage
        or 'Booking Created'

    )

    garage_status = (

        latest_booking.garage_status
        or latest_booking.service_status
        or 'Processing'

    )

    estimated_delivery = (

        latest_booking.estimated_delivery
        or 'Updating Soon'

    )

    active_message = (

        latest_booking.service_note
        or 'Service currently running.'
    )

    # ====================================
    # WORK DETAILS
    # ====================================

    current_work = (

        latest_booking.current_work
        or 'Work update pending.'
    )

    completed_work = (

        latest_booking.completed_work
        or 'No completed work.'
    )

    pending_work = (

        latest_booking.pending_work
        or 'Pending update soon.'
    )

    next_step = (

        latest_booking.next_step
        or 'Next update coming soon.'
    )

    # ====================================
    # PICKUP MESSAGE
    # ====================================

    pickup_message = None

    if latest_booking.pickup_ready:

        pickup_message = (

            latest_booking.pickup_message
            or
            'Vehicle Ready For Pickup'
        )

    # ====================================
    # NOTIFICATIONS
    # ====================================

    latest_notification = (

        latest_booking.latest_notification
        or
        'No New Notifications'
    )

    notification_time = (

        latest_booking.notification_time
        or ''
    )

    unread_notification = (

        latest_booking.unread_notification
    )

    # ====================================
    # STATUS COLOR
    # ====================================

    if latest_booking.pickup_ready:

        status_color = '#4dff88'

    elif progress_percentage >= 60:

        status_color = '#39cfff'

    else:

        status_color = '#ffb347'

    # ====================================
    # VEHICLE STATUS TEXT
    # ====================================

    if latest_booking.pickup_ready:

        vehicle_status_text = (
            'Ready For Pickup'
        )

    elif progress_percentage >= 80:

        vehicle_status_text = (
            'Final Stage'
        )

    elif progress_percentage >= 40:

        vehicle_status_text = (
            'Work In Progress'
        )

    else:

        vehicle_status_text = (
            'Service Started'
        )

    # ====================================
    # TOTAL UPDATES
    # ====================================

    total_updates = len(
        service_updates
    )

    # ====================================
    # LAST UPDATE
    # ====================================

    last_update = None

    if service_updates:

        last_update = service_updates[0]

    # ====================================
    # RENDER PAGE
    # ====================================

    return render_template(

        'tracking/tracking.html',

        booking=latest_booking,

        user=current_user,

        service_updates=service_updates,

        total_updates=total_updates,

        last_update=last_update,

        progress_percentage=progress_percentage,

        tracking_steps=tracking_steps,

        current_stage=current_stage,

        estimated_delivery=estimated_delivery,

        garage_status=garage_status,

        pickup_message=pickup_message,

        active_message=active_message,

        current_work=current_work,

        completed_work=completed_work,

        pending_work=pending_work,

        next_step=next_step,

        latest_notification=latest_notification,

        notification_time=notification_time,

        unread_notification=unread_notification,

        status_color=status_color,

        vehicle_status_text=vehicle_status_text
    )

@tracking.route(
    '/submit-rating',
    methods=['POST']
)
@login_required
def submit_rating():

    booking = Booking.query.filter_by(

        user_id=current_user.id

    ).order_by(

        Booking.id.desc()

    ).first()

    booking.rating = int(
        request.form.get(
            'rating'
        )
    )

    booking.review = request.form.get(
        'review'
    )

    booking.rating_submitted = True

    db.session.commit()

    flash(
        'Thank You For Rating'
    )

    return redirect(
        url_for(
            'tracking.tracking_page'
        )
    )