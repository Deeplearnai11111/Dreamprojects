from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required
from flask_login import current_user

from app import db

from app.models.user import User
from app.models.car import Car
from app.models.booking import Booking
from app.models.plan import Plan
from app.models.slot import Slot
from app.models.frequency import Frequency
from app.models.service_update import ServiceUpdate
from app.models.audit_log import AuditLog
from sqlalchemy import or_


admin = Blueprint(
    'admin',
    __name__
)


# ====================================
# ADMIN DASHBOARD
# ====================================

@admin.route('/admin/dashboard')
@login_required
def admin_dashboard():

    # ====================================
    # ADMIN / SUPER ADMIN ACCESS
    # ====================================

    if current_user.role not in [
        'admin',
        'super_admin'
    ]:

        flash(
            'Access Denied'
        )

        return redirect(
            url_for(
                'plans.plans_page'
            )
        )

    # ====================================
    # DATA
    # ====================================

    users = User.query.order_by(
        User.id.desc()
    ).all()

    bookings = Booking.query.order_by(
        Booking.id.desc()
    ).all()

    plans = Plan.query.order_by(
        Plan.id.desc()
    ).all()

    frequencies = Frequency.query.order_by(
        Frequency.id.desc()
    ).all()

    slots = Slot.query.order_by(
        Slot.id.desc()
    ).all()

    # ====================================
    # COUNTS
    # ====================================

    total_users = User.query.count()

    total_cars = Car.query.count()

    total_bookings = Booking.query.count()

    total_plans = Plan.query.count()

    active_services = Booking.query.filter_by(
        service_status='In Progress'
    ).count()

    completed_services = Booking.query.filter_by(
        service_status='Completed'
    ).count()

    # ====================================
    # REVENUE
    # ====================================

    paid_bookings = Booking.query.filter_by(
        payment_status='Paid'
    ).all()

    total_revenue = sum(
        booking.plan_price or 0
        for booking in paid_bookings
    )

    # ====================================
    # PAGE
    # ====================================

    return render_template(

        'admin/dashboard.html',

        users=users,

        bookings=bookings,

        plans=plans,

        frequencies=frequencies,

        slots=slots,

        total_users=total_users,

        total_cars=total_cars,

        total_bookings=total_bookings,

        total_plans=total_plans,

        active_services=active_services,

        completed_services=completed_services,

        total_revenue=total_revenue
    )


# ====================================
# CREATE FREQUENCY
# ====================================

@admin.route(
    '/admin/create-frequency',
    methods=['POST']
)
@login_required
def create_frequency():

    if not current_user.is_admin:

        return redirect(
            url_for('plans.plans_page')
        )

    frequency = Frequency(

        name=request.form.get(
            'name'
        ),

        subtitle=request.form.get(
            'subtitle'
        ),

        washes_per_month=int(
            request.form.get(
                'washes_per_month'
            ) or 0
        ),

        is_active=True
    )

    db.session.add(frequency)

    db.session.commit()

    flash('Frequency Created')

    return redirect(
        url_for('admin.admin_dashboard')
    )


# ====================================
# TOGGLE FREQUENCY
# ====================================

@admin.route(
    '/admin/toggle-frequency/<int:frequency_id>'
)
@login_required
def toggle_frequency(frequency_id):

    if not current_user.is_admin:

        return redirect(
            url_for('plans.plans_page')
        )

    frequency = Frequency.query.get_or_404(
        frequency_id
    )

    frequency.is_active = (
        not frequency.is_active
    )

    db.session.commit()

    flash('Frequency Updated')

    return redirect(
        url_for('admin.admin_dashboard')
    )


# ====================================
# DELETE FREQUENCY
# ====================================

@admin.route(
    '/admin/delete-frequency/<int:frequency_id>'
)
@login_required
def delete_frequency(frequency_id):

    if not current_user.is_admin:

        return redirect(
            url_for('plans.plans_page')
        )

    frequency = Frequency.query.get_or_404(
        frequency_id
    )

    db.session.delete(frequency)

    db.session.commit()

    flash('Frequency Deleted Successfully')

    return redirect(
        url_for('admin.admin_dashboard')
    )


# ====================================
# CREATE PLAN
# ====================================

@admin.route(
    '/admin/create-plan',
    methods=['POST']
)
@login_required
def create_plan():

    if not current_user.is_admin:

        return redirect(
            url_for('plans.plans_page')
        )

    frequency_id = request.form.get(
        'frequency_id'
    )

    if not frequency_id:

        flash('Frequency Missing')

        return redirect(
            url_for('admin.admin_dashboard')
        )

    plan = Plan(

        frequency_id=int(
            frequency_id
        ),

        name=request.form.get(
            'name'
        ),

        subtitle=request.form.get(
            'subtitle'
        ),

        price=int(
            request.form.get(
                'price'
            ) or 0
        ),

        badge=request.form.get(
            'badge'
        ),

        theme=request.form.get(
            'theme'
        ) or 'prime',

        is_active=True
    )

    db.session.add(plan)

    db.session.commit()

    flash('Plan Created')

    return redirect(
        url_for('admin.admin_dashboard')
    )


# ====================================
# TOGGLE PLAN
# ====================================

@admin.route(
    '/admin/toggle-plan/<int:plan_id>'
)
@login_required
def toggle_plan(plan_id):

    if not current_user.is_admin:

        return redirect(
            url_for('plans.plans_page')
        )

    plan = Plan.query.get_or_404(
        plan_id
    )

    plan.is_active = (
        not plan.is_active
    )

    db.session.commit()

    flash('Plan Updated')

    return redirect(
        url_for('admin.admin_dashboard')
    )


# ====================================
# DELETE PLAN
# ====================================

@admin.route(
    '/admin/delete-plan/<int:plan_id>'
)
@login_required
def delete_plan(plan_id):

    if not current_user.is_admin:

        return redirect(
            url_for('plans.plans_page')
        )

    plan = Plan.query.get_or_404(
        plan_id
    )

    db.session.delete(plan)

    db.session.commit()

    flash('Plan Deleted')

    return redirect(
        url_for('admin.admin_dashboard')
    )


# ====================================
# CREATE SLOT
# ====================================

@admin.route(
    '/admin/create-slot',
    methods=['POST']
)
@login_required
def create_slot():

    # ====================================
    # SECURITY
    # ====================================

    if not current_user.is_admin:

        flash('Access Denied')

        return redirect(
            url_for('plans.plans_page')
        )

    # ====================================
    # FORM DATA
    # ====================================

    frequency_id = request.form.get(
        'frequency_id'
    )

    plan_id = request.form.get(
        'plan_id'
    )

    slot_times = request.form.get(
        'slot_times'
    )

    shift = (
    request.form.get('shift') or
    request.form.get('slot_type') or
    'Morning'
).strip()

    slot_type = request.form.get(
        'slot_type'
    ) or shift

    max_bookings = request.form.get(
        'max_bookings'
    )

    # ====================================
    # VALIDATION
    # ====================================

    if not frequency_id:

        flash('Frequency ID Missing')

        return redirect(
            url_for('admin.admin_dashboard')
        )

    if not plan_id:

        flash('Plan ID Missing')

        return redirect(
            url_for('admin.admin_dashboard')
        )

    if not slot_times:

        flash('Slot Time Missing')

        return redirect(
            url_for('admin.admin_dashboard')
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

        max_bookings = int(
            max_bookings or 10
        )

    except ValueError:

        flash('Invalid Numeric Value')

        return redirect(
            url_for('admin.admin_dashboard')
        )

    # ====================================
    # MULTIPLE SLOT SUPPORT
    # ====================================

    slot_list = [

        slot.strip()

        for slot in slot_times.splitlines()

        if slot.strip()

    ]

    created_count = 0

    # ====================================
    # CREATE ALL SLOTS
    # ====================================

    for single_slot in slot_list:

        # ====================================
        # DUPLICATE CHECK
        # ====================================

        existing_slot = Slot.query.filter_by(

            frequency_id=frequency_id,

            plan_id=plan_id,

            slot_time=single_slot,

            shift=shift

        ).first()

        if existing_slot:

            continue

        # ====================================
        # CREATE SLOT
        # ====================================

        slot = Slot(

            frequency_id=frequency_id,

            plan_id=plan_id,

            slot_time=single_slot,

            shift=shift,

            slot_type=slot_type,

            slot_label=f'{shift} Slot',

            max_bookings=max_bookings,

            current_bookings=0,

            remaining_slots=max_bookings,

            status='Open',

            is_active=True,

            is_full=False,

            is_priority=True
            if request.form.get(
                'is_priority'
            )
            else False,

            is_recommended=True
            if request.form.get(
                'is_recommended'
            )
            else False,

            slot_color=request.form.get(
                'slot_color'
            ) or '#39cfff'
        )

        db.session.add(slot)

        created_count += 1

    # ====================================
    # SAVE
    # ====================================

    db.session.commit()

    flash(
        f'{created_count} Slot(s) Created Successfully'
    )

    return redirect(
        url_for('admin.admin_dashboard')
    )


# ====================================
# TOGGLE SLOT
# ====================================

@admin.route(
    '/admin/toggle-slot/<int:slot_id>'
)
@login_required
def toggle_slot(slot_id):

    if not current_user.is_admin:

        return redirect(
            url_for('plans.plans_page')
        )

    slot = Slot.query.get_or_404(
        slot_id
    )

    slot.is_active = (
        not slot.is_active
    )

    if slot.is_active:

        slot.status = 'Open'

    else:

        slot.status = 'Closed'

    db.session.commit()

    flash('Slot Updated')

    return redirect(
        url_for('admin.admin_dashboard')
    )


# ====================================
# DELETE SLOT
# ====================================

@admin.route(
    '/admin/delete-slot/<int:slot_id>'
)
@login_required
def delete_slot(slot_id):

    if not current_user.is_admin:

        return redirect(
            url_for('plans.plans_page')
        )

    slot = Slot.query.get_or_404(
        slot_id
    )

    db.session.delete(slot)

    db.session.commit()

    flash('Slot Deleted')

    return redirect(
        url_for('admin.admin_dashboard')
    )


# ====================================
# UPDATE PAYMENT
# ====================================

@admin.route(
    '/admin/update-payment/<int:booking_id>',
    methods=['POST']
)
@login_required
def update_payment(booking_id):

    booking = Booking.query.get_or_404(
        booking_id
    )

    booking.payment_status = request.form.get(
        'payment_status'
    )

    db.session.commit()

    flash('Payment Updated')

    return redirect(
        url_for('admin.admin_dashboard')
    )


# ====================================
# UPDATE SERVICE STATUS
# ====================================

@admin.route(
    '/admin/update-status/<int:booking_id>',
    methods=['POST']
)
@login_required
def update_status(booking_id):

    booking = Booking.query.get_or_404(
        booking_id
    )

    progress_percentage = int(
        request.form.get(
            'progress_percentage'
        ) or 0
    )

    booking.progress_percentage = (
        progress_percentage
    )

    booking.service_stage = request.form.get(
        'service_stage'
    )

    booking.service_note = request.form.get(
        'service_note'
    )

    if progress_percentage >= 100:

        booking.service_status = (
            'Completed'
        )

    else:

        booking.service_status = (
            'In Progress'
        )

    service_update = ServiceUpdate(

        booking_id=booking.id,

        stage=booking.service_stage,

        description=booking.service_note,

        progress=progress_percentage
    )

    db.session.add(service_update)

    db.session.commit()

    flash('Service Updated')

    return redirect(
        url_for('admin.admin_dashboard')
    )


@admin.route(
    '/update-stage/<int:booking_id>/<stage>'
)
@login_required
def update_stage(
    booking_id,
    stage
):

    booking = Booking.query.get_or_404(
        booking_id
    )

    booking.service_stage = stage

    if stage == "Arrived":
        booking.progress_percentage = 50

    elif stage == "Cleaning":
        booking.progress_percentage = 75

    elif stage == "Done":
        booking.progress_percentage = 100

    db.session.commit()

    flash(
        f"Status Updated: {stage}"
    )

    # prefer returning to referring page (bookings/service control), fallback to admin bookings
    return redirect(
        request.referrer or url_for('admin.admin_bookings')
    )



@admin.route('/admin/service-control')
@login_required
def service_control():

    if not current_user.is_admin:

        return redirect(url_for('plans.plans_page'))

    bookings = Booking.query.order_by(Booking.id.desc()).all()

    return render_template('admin/service_control.html', bookings=bookings)


# ====================================
# SUPER-ADMIN UNLOCK (for admins to access super-admin panel)
# ====================================


@admin.route(
    '/admin/unlock-super',
    methods=['POST']
)
@login_required
def unlock_super():

    # only admins (not regular users) may attempt to unlock
    if not current_user.is_admin:

        return redirect(url_for('plans.plans_page'))

    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:

        flash('Enter super admin credentials')

        return redirect(url_for('admin.admin_dashboard'))

    super_user = User.query.filter_by(email=username, role='super_admin').first() or User.query.filter_by(full_name=username, role='super_admin').first()

    if not super_user or not super_user.check_password(password):

        flash('Invalid super admin credentials')

        return redirect(url_for('admin.admin_dashboard'))

    # grant temporary unlock in session
    from flask import session

    session['super_admin_unlocked'] = True

    # log unlock attempt
    try:
        log = AuditLog(
            actor=current_user.full_name,
            action='Unlock Super Admin',
            details=f'Admin {current_user.id} unlocked super-admin using {super_user.email if super_user else username}'
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        db.session.rollback()

    return redirect(url_for('admin.super_admin_panel'))


# ====================================
# SUPER-ADMIN PANEL
# ====================================


@admin.route('/admin/super-admin')
@login_required
def super_admin_panel():

    from flask import session

    # allow real super_admins or admins who unlocked with credentials
    unlocked = session.get('super_admin_unlocked')

    if not (current_user.role == 'super_admin' or unlocked):

        flash('Access Denied')

        return redirect(url_for('admin.admin_dashboard'))

    users = User.query.order_by(User.id.desc()).all()

    return render_template('admin/super_admin.html', users=users)



@admin.route('/admin/super-admin/manage-admins')
@login_required
def super_admin_manage_admins():

    from flask import session

    unlocked = session.get('super_admin_unlocked')

    if not (current_user.role == 'super_admin' or unlocked):

        flash('Access Denied')

        return redirect(url_for('admin.admin_dashboard'))

    admins = User.query.filter(User.role.in_(['admin','super_admin'])).order_by(User.id.desc()).all()

    return render_template('admin/super_admin_manage_admins.html', admins=admins)


@admin.route('/admin/super-admin/edit-admin/<int:user_id>', methods=['GET','POST'])
@login_required
def super_admin_edit_admin(user_id):

    from flask import session

    unlocked = session.get('super_admin_unlocked')

    if not (current_user.role == 'super_admin' or unlocked):

        flash('Access Denied')

        return redirect(url_for('admin.admin_dashboard'))

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':

        user.full_name = request.form.get('full_name') or user.full_name

        user.email = request.form.get('email') or user.email

        new_password = request.form.get('password')

        if new_password:

            user.set_password(new_password)

        db.session.commit()

        # audit
        try:
            log = AuditLog(
                actor=current_user.full_name,
                action='Edit Admin Credentials',
                details=f'Edited admin {user.id} ({user.email})'
            )
            db.session.add(log)
            db.session.commit()
        except Exception:
            db.session.rollback()

        flash('Admin Updated')

        return redirect(url_for('admin.super_admin_manage_admins'))

    return render_template('admin/super_admin_edit_admin.html', user=user)


@admin.route('/admin/super-admin/user/<int:user_id>')
@login_required
def super_admin_user_detail(user_id):

    from flask import session

    unlocked = session.get('super_admin_unlocked')

    if not (current_user.role == 'super_admin' or unlocked):

        flash('Access Denied')

        return redirect(url_for('admin.admin_dashboard'))

    user = User.query.get_or_404(user_id)

    return render_template('admin/user_detail.html', user=user)


@admin.route('/admin/super-admin/logs')
@login_required
def super_admin_logs():

    from flask import session

    unlocked = session.get('super_admin_unlocked')

    if not (current_user.role == 'super_admin' or unlocked):

        flash('Access Denied')

        return redirect(url_for('admin.admin_dashboard'))

    logs = AuditLog.query.order_by(AuditLog.id.desc()).limit(500).all()

    return render_template('admin/super_admin_logs.html', logs=logs)


@admin.route('/admin/super-admin/delete-user/<int:user_id>', methods=['POST'])
@login_required
def super_admin_delete_user(user_id):

    from flask import session

    if current_user.role != 'super_admin' and not session.get('super_admin_unlocked'):

        flash('Access Denied')

        return redirect(url_for('admin.admin_dashboard'))

    user = User.query.get_or_404(user_id)

    db.session.delete(user)

    db.session.commit()

    # audit
    try:
        log = AuditLog(
            actor=current_user.full_name,
            action='Delete User',
            details=f'Deleted user {user.id} ({user.email})'
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        db.session.rollback()

    flash('User Deleted')

    return redirect(url_for('admin.super_admin_panel'))


# ====================================
# CHANGE PASSWORD (for admin and super_admin)
# ====================================


@admin.route('/admin/change-password', methods=['GET', 'POST'])
@login_required
def admin_change_password():

    if not current_user.is_admin:

        return redirect(url_for('plans.plans_page'))

    if request.method == 'POST':

        old = request.form.get('old_password')

        new = request.form.get('new_password')

        if not old or not new:

            flash('Fill all fields')

            return redirect(url_for('admin.admin_change_password'))

        if not current_user.check_password(old):

            flash('Old password incorrect')

            return redirect(url_for('admin.admin_change_password'))

        current_user.set_password(new)

        db.session.commit()

        flash('Password Updated')

        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/change_password.html')


# ====================================
# BOOKINGS MANAGEMENT
# ====================================


@admin.route('/admin/bookings')
@login_required
def admin_bookings():

    if not current_user.is_admin:

        return redirect(url_for('plans.plans_page'))

    bookings = Booking.query.order_by(Booking.id.desc()).all()

    return render_template('admin/bookings.html', bookings=bookings)


# ====================================
# BOOKINGS BY USER (search + list)
# ====================================


@admin.route('/admin/user-bookings')
@login_required
def admin_user_bookings():

    if not current_user.is_admin:

        return redirect(url_for('plans.plans_page'))

    q = request.args.get('q')

    if q:

        # search by full name or email
        users = User.query.filter(
            or_(
                User.full_name.ilike(f"%{q}%"),
                User.email.ilike(f"%{q}%")
            )
        ).order_by(User.id.desc()).all()

    else:

        users = User.query.order_by(User.id.desc()).all()

    return render_template('admin/user_bookings.html', users=users, query=q)


@admin.route('/admin/user-bookings/<int:user_id>')
@login_required
def admin_user_bookings_detail(user_id):

    if not current_user.is_admin:

        return redirect(url_for('plans.plans_page'))

    user = User.query.get_or_404(user_id)

    bookings = Booking.query.filter_by(user_id=user.id).order_by(Booking.id.desc()).all()

    return render_template('admin/user_bookings_detail.html', user=user, bookings=bookings)


@admin.route('/admin/booking/<int:booking_id>')
@login_required
def admin_booking_detail(booking_id):

    if not current_user.is_admin:

        return redirect(url_for('plans.plans_page'))

    booking = Booking.query.get_or_404(booking_id)

    updates = ServiceUpdate.query.filter_by(booking_id=booking.id).order_by(ServiceUpdate.id.desc()).all()

    return render_template('admin/booking_detail.html', booking=booking, updates=updates)


@admin.route('/admin/booking/<int:booking_id>/update-stage', methods=['POST'])
@login_required
def admin_booking_update_stage(booking_id):

    if not current_user.is_admin:

        return redirect(url_for('plans.plans_page'))

    booking = Booking.query.get_or_404(booking_id)

    stage = request.form.get('stage')

    note = request.form.get('note')

    if stage:

        booking.service_stage = stage

        if stage == 'Arrived':

            booking.progress_percentage = 50

        elif stage == 'Cleaning':

            booking.progress_percentage = 75

        elif stage == 'Done':

            booking.progress_percentage = 100

    if note:

        booking.service_note = note

    service_update = ServiceUpdate(

        booking_id=booking.id,

        stage=booking.service_stage,

        description=booking.service_note,

        progress=booking.progress_percentage

    )

    db.session.add(service_update)

    db.session.commit()

    # audit
    try:
        log = AuditLog(
            actor=current_user.full_name,
            action='Update Booking Stage',
            details=f'Booking {booking.id} updated to {booking.service_stage} by {current_user.id} with note: {booking.service_note}'
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        db.session.rollback()

    flash('Booking Updated')

    return redirect(url_for('admin.admin_booking_detail', booking_id=booking.id))



@admin.route('/admin/delete-booking/<int:booking_id>', methods=['POST'])
@login_required
def admin_delete_booking(booking_id):

    if not current_user.is_admin:

        return redirect(url_for('plans.plans_page'))

    booking = Booking.query.get_or_404(booking_id)

    # delete related service updates
    ServiceUpdate.query.filter_by(booking_id=booking.id).delete()

    db.session.delete(booking)

    db.session.commit()

    # audit
    try:
        log = AuditLog(
            actor=current_user.full_name,
            action='Delete Booking',
            details=f'Deleted booking {booking.id} for user {booking.user_id}'
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        db.session.rollback()

    flash('Booking Deleted')

    return redirect(url_for('admin.service_control'))