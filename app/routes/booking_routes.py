

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import flash

from flask_login import login_required
from flask_login import current_user

from app import db

from app.models.frequency import Frequency
from app.models.plan import Plan
from app.models.slot import Slot
from app.models.booking import Booking


booking = Blueprint(
    'booking',
    __name__
)

@booking.route(
    '/schedule',
    methods=['GET', 'POST']
)
@login_required
def schedule():
    from flask import current_app

    current_app.logger.info(f"SCHEDULE ROUTE CALLED: method={request.method}")

    # ====================================
    # FORM SUBMIT
    # ====================================

    if request.method == 'POST':
        # Temporary debug prints to ensure we see POST flow in terminal
        print("=== SCHEDULE POST ENTER ===", flush=True)
        print("Headers:", dict(request.headers), flush=True)
        print("Form:", dict(request.form), flush=True)
        current_app.logger.info("POST RECEIVED %s", dict(request.form))

        frequency_id = request.form.get(
            'frequency_id'
        )

        plan_id = request.form.get(
            'plan_id'
        )

        slot_id = request.form.get(
            'slot_id'
        )

        from flask import current_app

        current_app.logger.debug("frequency_id=%s plan_id=%s slot_id=%s", frequency_id, plan_id, slot_id)

        # ====================================
        # VALIDATION
        # ====================================

        if not frequency_id:

            flash(
                'Please Select Frequency'
            )

            return redirect(
                url_for('booking.schedule')
            )

        if not plan_id:

            flash(
                'Please Select Plan'
            )

            return redirect(
                url_for('booking.schedule')
            )

        if not slot_id:

            flash(
                'Please Select Slot'
            )

            return redirect(
                url_for('booking.schedule')
            )

        # ====================================
        # SAFE INTEGER CONVERSION
        # ====================================

        try:

            frequency_id = int(
                frequency_id
            )

            plan_id = int(
                plan_id
            )

            slot_id = int(
                slot_id
            )

        except ValueError:
            print("=== SCHEDULE POST: invalid int conversion ===", flush=True)

            flash(
                'Invalid Selection'
            )

            return redirect(
                url_for('booking.schedule')
            )

        # ====================================
        # FETCH DATABASE OBJECTS
        # ====================================

        frequency = Frequency.query.get(
            frequency_id
        )

        plan = Plan.query.get(
            plan_id
        )

        slot = Slot.query.get(
            slot_id
        )

        # ====================================
        # OBJECT VALIDATION
        # ====================================

        if not frequency:

            flash(
                'Frequency Not Found'
            )

            return redirect(
                url_for('booking.schedule')
            )

        if not plan:

            flash(
                'Plan Not Found'
            )

            return redirect(
                url_for('booking.schedule')
            )

        if not slot:

            flash(
                'Slot Not Found'
            )

            return redirect(
                url_for('booking.schedule')
            )

        # ====================================
        # SLOT FULL CHECK
        # ====================================

        if slot.is_full:

            flash(
                'Selected Slot is Full'
            )

            return redirect(
                url_for('booking.schedule')
            )

        # ====================================
        # CREATE BOOKING
        # ====================================

        new_booking = Booking(

    user_id=current_user.id,

    plan_name=plan.name,

    plan_price=plan.price,

    slot_id=slot.id,

    service_time=slot.slot_time,

    frequency=frequency.name,

    booking_status='Confirmed',

    payment_status='Pending',

    service_status='Scheduled'
)

        
        

        # ====================================
        # UPDATE SLOT
        # ====================================

        slot.current_bookings += 1

        slot.remaining_slots = (

            slot.max_bookings -
            slot.current_bookings

        )

        if (

            slot.current_bookings >=
            slot.max_bookings

        ):

            slot.is_full = True

            slot.status = 'Full'

        # ====================================
        # SAVE
        # ====================================

        db.session.add(
            new_booking
        )

        print("=== SCHEDULE POST: BEFORE COMMIT ===", flush=True)
        current_app.logger.info("BEFORE COMMIT")

        db.session.commit()

        print("=== SCHEDULE POST: AFTER COMMIT ===", flush=True)
        print("=== NEW BOOKING ID ===", new_booking.id, flush=True)
        current_app.logger.info("AFTER COMMIT")
        current_app.logger.info("NEW BOOKING ID = %s", new_booking.id)

        flash('Schedule Confirmed Successfully')

        # Temporary DEBUG: return JSON so browser Network shows exact response
        return redirect(
    url_for(
        'payment.payment_page',
        booking_id=new_booking.id
    )
)

    # ====================================
    # GET PAGE
    # ====================================

    frequencies = Frequency.query.filter_by(
        is_active=True
    ).all()

    plans = Plan.query.filter_by(
        is_active=True
    ).all()

    slots = Slot.query.filter_by(
        is_active=True
    ).order_by(
        Slot.id.asc()
    ).all()

    return render_template(

        'booking/schedule.html',

        frequencies=frequencies,

        plans=plans,

        slots=slots
    )