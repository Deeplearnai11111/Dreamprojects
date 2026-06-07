from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import current_app

from flask_login import login_required
from flask_login import current_user

from app import db

from app.models.booking import Booking


payment = Blueprint(
    'payment',
    __name__
)


# ====================================
# PAYMENT PAGE
# ====================================

@payment.route(
    '/payment',
    methods=['GET', 'POST']
)
@login_required
def payment_page():

    # ====================================
    # GET BOOKING ID
    # ====================================

    booking_id = request.args.get('booking_id')

    current_app.logger.debug("payment_page: booking_id param=%s", booking_id)

    # ====================================
    # FIND BOOKING
    # ====================================

    if booking_id:
        try:
            bid = int(booking_id)
        except Exception:
            bid = None

        booking = Booking.query.filter_by(id=bid, user_id=current_user.id).first() if bid else None

    else:

        booking = Booking.query.filter_by(

            user_id=current_user.id

        ).order_by(

            Booking.id.desc()

        ).first()

    current_app.logger.debug("payment_page: booking found=%s booking.id=%s", bool(booking), getattr(booking, 'id', None))

    # ====================================
    # SECURITY
    # ====================================

    if not booking:

        flash(
            'Booking Not Found'
        )

        return redirect(
            url_for(
                'booking.schedule'
            )
        )

    # ====================================
    # ALREADY PAID
    # ====================================

    if booking.payment_status == 'Paid':

        flash(
            'Payment Already Completed'
        )

        return redirect(
            url_for(
                 'tracking.tracking_page'
            )
        )

    # ====================================
    # PAYMENT SUBMIT
    # ====================================

    if request.method == 'POST':

        # ====================================
        # FORM DATA
        # ====================================

        payment_method = request.form.get(
            'payment_method'
        )

        transaction_id = request.form.get(
            'transaction_id'
        )

        # ====================================
        # VALIDATION
        # ====================================

        

        if not transaction_id:

            flash(
                'Enter Transaction ID'
            )

            return redirect(
                url_for(
                    'payment.payment_page',
                    booking_id=booking.id
                )
            )

        # ====================================
        # UPDATE PAYMENT
        # ====================================

        booking.payment_method = (
        payment_method
      )

        booking.transaction_id = (
        transaction_id
      )

        # ====================================
        # PAYMENT STATUS
        # ====================================

        booking.payment_status = 'Paid'
        booking.is_payment_completed = True

        # ====================================
        # BOOKING STATUS
        # ====================================

        booking.booking_status = 'Confirmed'
        booking.service_status = 'Scheduled'

        # ====================================
        # TRACKING STATUS
        # ====================================

        booking.service_stage = 'Assigned'
        booking.progress_percentage = 25

        # ====================================
        # DEFAULT TRACKING MESSAGE
        # ====================================

        booking.service_note = 'Booking confirmed and assigned to CLEANZO team.'

        # ====================================
        # SAVE DATABASE
        # ====================================

        db.session.commit()

        # ====================================
        # SUCCESS
        # ====================================

        flash('Payment Successful')

        # Render payment page with success flag so frontend can show confirmation modal
        total_price = booking.plan_price

        return render_template(
            'payments/payment.html',
            booking=booking,
            total_price=total_price,
            user=current_user,
            success=True,
            transaction_id=transaction_id
        )

    # ====================================
    # FINAL PRICE CALCULATION
    # ====================================

    total_price = booking.plan_price

    # ====================================
    # PAGE
    # ====================================

    return render_template(

        'payments/payment.html',

        booking=booking,

        total_price=total_price,

        user=current_user
    )