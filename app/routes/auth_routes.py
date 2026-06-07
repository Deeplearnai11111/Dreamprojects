from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session

from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user

from app import db
from app import oauth
import os
import smtplib
import ssl
import random
from email.message import EmailMessage
from datetime import datetime, timedelta

from app.models.user import User
from app.models.car import Car
from app.models.plan import Plan
from app.models.slot import Slot
from app.models.frequency import Frequency
from app.models.booking import Booking


auth = Blueprint(
    'auth',
    __name__
)


def send_email(subject, recipient, body):
    mail_server = os.environ.get('MAIL_SERVER')
    mail_port = int(os.environ.get('MAIL_PORT', '587'))
    mail_username = os.environ.get('MAIL_USERNAME')
    mail_password = os.environ.get('MAIL_PASSWORD')
    mail_use_tls = os.environ.get('MAIL_USE_TLS', 'true').lower() in ('true', '1', 'yes')
    mail_use_ssl = os.environ.get('MAIL_USE_SSL', 'false').lower() in ('true', '1', 'yes')
    from_email = os.environ.get('MAIL_DEFAULT_SENDER', mail_username or 'noreply@cleanzo.in')

    if not mail_server or not mail_username or not mail_password:
        print('Mail config missing, cannot send email')
        return False

    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = recipient
    message.set_content(body)

    try:
        if mail_use_ssl:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(mail_server, mail_port, context=context) as smtp:
                smtp.login(mail_username, mail_password)
                smtp.send_message(message)
        else:
            with smtplib.SMTP(mail_server, mail_port) as smtp:
                if mail_use_tls:
                    smtp.starttls(context=ssl.create_default_context())
                smtp.login(mail_username, mail_password)
                smtp.send_message(message)
        return True
    except Exception as exc:
        print('Email send failed:', exc)
        return False


# ====================================
# HOME PAGE
# ====================================

@auth.route('/')
def home():

    if current_user.is_authenticated:

        if current_user.is_admin:

            return redirect(
                url_for(
                    'admin.admin_dashboard'
                )
            )

        return redirect(
            url_for(
                'auth.dashboard'
            )
        )

    return render_template(
        'home/index.html'
    )


# ====================================
# REGISTER
# ====================================

@auth.route(
    '/register',
    methods=['GET', 'POST']
)
def register():

    if current_user.is_authenticated:

        return redirect(
            url_for(
                'auth.dashboard'
            )
        )

    if request.method == 'POST':

        # USER DATA

        full_name = request.form.get(
            'full_name'
        )

        phone = request.form.get(
            'phone'
        )

        email = request.form.get(
            'email'
        )

        society = request.form.get(
            'society'
        )

        block = request.form.get(
            'block'
        )

        flat_number = request.form.get(
            'flat_number'
        )

        password = request.form.get(
            'password'
        )

        # CAR DATA

        car_brand = request.form.get(
            'car_brand'
        )

        car_model = request.form.get(
            'car_model'
        )

        car_color = request.form.get(
            'car_color'
        )

        car_registration = request.form.get(
            'car_registration'
        )

        # VALIDATION

        if not full_name or not phone or not password:

            flash(
                'Please Fill Required Fields'
            )

            return redirect(
                url_for(
                    'auth.register'
                )
            )

        # PHONE CHECK

        existing_user = User.query.filter_by(
            phone=phone
        ).first()

        if existing_user:

            flash(
                'Phone Already Registered'
            )

            return redirect(
                url_for(
                    'auth.register'
                )
            )

        # EMAIL CHECK

        if email:

            existing_email = User.query.filter_by(
                email=email
            ).first()

            if existing_email:

                flash(
                    'Email Already Registered'
                )

                return redirect(
                    url_for(
                        'auth.register'
                    )
                )

        # CREATE USER

        user = User(

            full_name=full_name,

            phone=phone,

            email=email,

            society=society,

            block=block,

            flat_number=flat_number,

            is_admin=False,

            active_plan='No Plan',

            account_status='Active',

            customer_type='Regular'
        )

        user.set_password(
            password
        )

        db.session.add(user)

        db.session.commit()

        # CREATE CAR

        if car_registration:

            car = Car(

                user_id=user.id,

                registration_number=car_registration,

                car_model=car_model,

                car_brand=car_brand,

                car_colour=car_color
            )

            db.session.add(car)

            db.session.commit()

        # LOGIN

        login_user(

            user,

            remember=True
        )

        # generate and store a session token so other sessions are invalidated
        import uuid
        token = uuid.uuid4().hex
        user.session_token = token
        db.session.commit()
        session['session_token'] = token

        flash(
            'Registration Successful'
        )

        return redirect(
            url_for(
                'auth.dashboard'
            )
        )

    return render_template(
        'auth/register.html'
    )


# ====================================
# LOGIN
# ====================================

@auth.route(
    '/login',
    methods=['GET', 'POST']
)
def login():

    if current_user.is_authenticated:

        if current_user.is_admin:

            return redirect(
                url_for(
                    'admin.admin_dashboard'
                )
            )

        return redirect(
            url_for(
                'auth.dashboard'
            )
        )

    if request.method == 'POST':

        phone = request.form.get(
            'phone'
        )

        password = request.form.get(
            'password'
        )

        if not phone or not password:

            flash(
                'Enter Phone And Password'
            )

            return redirect(
                url_for(
                    'auth.login'
                )
            )

        # ====================================
        # ADMIN LOGIN
        # ====================================

        # Special handling for admin phone. Use environment password or stored hashed password.
        if phone == 'admin':
            admin_user = User.query.filter_by(phone='admin').first()
            env_admin_pass = os.environ.get('ADMIN_PASSWORD')

            # If admin user exists, verify against its hashed password
            if admin_user:
                if admin_user.check_password(password):
                    # ensure role is set
                    if admin_user.role != 'admin':
                        admin_user.role = 'admin'
                        db.session.commit()

                    login_user(admin_user, remember=True)
                    # set session token for admin session
                    import uuid
                    token = uuid.uuid4().hex
                    admin_user.session_token = token
                    db.session.commit()
                    session['session_token'] = token

                    flash('Admin Login Successful')

                    return redirect(url_for('admin.admin_dashboard'))
                else:
                    flash('Invalid Credentials')
                    return redirect(url_for('auth.login'))

            # No admin user exists: allow creation only if password matches env var
            if env_admin_pass and password == env_admin_pass:
                admin_user = User(
                    full_name='CLEANZO ADMIN',
                    phone='admin',
                    email='admin@cleanzo.in',
                    society='CLEANZO HQ',
                    block='ADMIN',
                    flat_number='001',
                    is_admin=True,
                    role='admin',
                    active_plan='ADMIN',
                    account_status='Active',
                    customer_type='Administrator'
                )
                admin_user.set_password(password)
                db.session.add(admin_user)
                db.session.commit()

                login_user(admin_user, remember=True)
                import uuid
                token = uuid.uuid4().hex
                admin_user.session_token = token
                db.session.commit()
                session['session_token'] = token

                flash('Admin Created and Logged In')
                return redirect(url_for('admin.admin_dashboard'))

            flash('Invalid Credentials')
            return redirect(url_for('auth.login'))

        # ====================================
        # USER LOGIN
        # ====================================

        user = User.query.filter_by(
            phone=phone
        ).first()

        if not user:

            flash(
                'Account Not Found'
            )

            return redirect(
                url_for(
                    'auth.login'
                )
            )

        if user.account_status == 'Blocked':

            flash(
                'Account Blocked'
            )

            return redirect(
                url_for(
                    'auth.login'
                )
            )

        if user.check_password(password):

            login_user(

                user,

                remember=True
            )

            # generate and store a session token so other sessions are invalidated
            import uuid
            token = uuid.uuid4().hex
            user.session_token = token
            db.session.commit()
            session['session_token'] = token

            flash(
                f'Welcome {user.full_name}'
            )

            if user.is_admin:

                return redirect(
                    url_for(
                        'admin.admin_dashboard'
                    )
                )

            return redirect(
                url_for(
                    'auth.dashboard'
                )
            )

        flash(
            'Invalid Credentials'
        )

        return redirect(
            url_for(
                'auth.login'
            )
        )

    return render_template(
        'auth/login.html'
    )


# ====================================
# FORGOT PASSWORD
# ====================================

@auth.route(
    '/forgot-password',
    methods=['GET', 'POST']
)
def forgot_password():

    if current_user.is_authenticated:

        return redirect(
            url_for(
                'auth.dashboard'
            )
        )

    if request.method == 'POST':

        email = request.form.get(
            'email'
        )

        if not email:

            flash(
                'Enter your email address'
            )

            return redirect(
                url_for(
                    'auth.forgot_password'
                )
            )

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:

            flash(
                'Email not found. Please register first.'
            )

            return redirect(
                url_for(
                    'auth.forgot_password'
                )
            )

        otp = str(random.randint(100000, 999999))
        expiry = datetime.utcnow() + timedelta(minutes=10)

        session['password_reset'] = {
            'email': email,
            'otp': otp,
            'expires': expiry.isoformat()
        }

        subject = 'CLEANZO Password Reset OTP'
        body = (
            f'Hello {user.full_name},\n\n'
            f'Use the following OTP to reset your CLEANZO password:\n\n'
            f'{otp}\n\n'
            'This OTP is valid for 10 minutes. If you did not request this, please ignore this email.\n\n'
            'Thank you,\nCLEANZO Team'
        )

        if send_email(subject, email, body):
            flash(
                'OTP sent to your email address.'
            )
        else:
            flash(
                'Unable to send OTP email right now. Check email settings.'
            )

        return redirect(
            url_for(
                'auth.reset_password'
            )
        )

    return render_template(
        'auth/forgot_password.html'
    )


# ====================================
# RESET PASSWORD
# ====================================

@auth.route(
    '/reset-password',
    methods=['GET', 'POST']
)
def reset_password():

    if current_user.is_authenticated:

        return redirect(
            url_for(
                'auth.dashboard'
            )
        )

    reset_data = session.get('password_reset')

    if not reset_data:
        flash(
            'Please request a password reset first.'
        )
        return redirect(
            url_for(
                'auth.forgot_password'
            )
        )

    expires = datetime.fromisoformat(
        reset_data.get('expires')
    )

    if datetime.utcnow() > expires:
        session.pop('password_reset', None)
        flash(
            'OTP expired. Please request a new one.'
        )
        return redirect(
            url_for(
                'auth.forgot_password'
            )
        )

    if request.method == 'POST':

        email = request.form.get(
            'email'
        )

        otp = request.form.get(
            'otp'
        )

        password = request.form.get(
            'password'
        )

        confirm_password = request.form.get(
            'confirm_password'
        )

        if not email or not otp or not password or not confirm_password:
            flash(
                'Please complete all fields.'
            )
            return redirect(
                url_for(
                    'auth.reset_password'
                )
            )

        if email != reset_data.get('email'):
            flash(
                'Email does not match the requested account.'
            )
            return redirect(
                url_for(
                    'auth.reset_password'
                )
            )

        if otp != reset_data.get('otp'):
            flash(
                'Invalid OTP. Please check your email.'
            )
            return redirect(
                url_for(
                    'auth.reset_password'
                )
            )

        if password != confirm_password:
            flash(
                'Passwords do not match.'
            )
            return redirect(
                url_for(
                    'auth.reset_password'
                )
            )

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:
            flash(
                'No account found for this email.'
            )
            return redirect(
                url_for(
                    'auth.forgot_password'
                )
            )

        user.set_password(password)
        import uuid
        token = uuid.uuid4().hex
        user.session_token = token
        db.session.commit()
        session['session_token'] = token
        session.pop('password_reset', None)
        login_user(user, remember=True)

        flash(
            'Password reset successful. You are now logged in.'
        )

        return redirect(
            url_for(
                'auth.dashboard'
            )
        )

    return render_template(
        'auth/reset_password.html',
        email=reset_data.get('email')
    )


# ====================================
# GOOGLE OAUTH
# ====================================


@auth.route('/login/google')
def google_login():
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth.route('/login/google/callback')
def google_callback():
    try:
        token = oauth.google.authorize_access_token()
    except Exception as e:
        # more helpful debug info
        print('Google authorize_access_token error:', repr(e))
        flash(f'Google login failed: {e}')
        return redirect(url_for('auth.login'))

    try:
        resp = oauth.google.get('userinfo')
        user_info = resp.json()
    except Exception as e:
        print('Google userinfo fetch error:', repr(e))
        flash(f'Google login failed: {e}')
        return redirect(url_for('auth.login'))

    email = user_info.get('email')
    name = user_info.get('name') or user_info.get('given_name') or 'Google User'
    picture = user_info.get('picture')

    user = None
    if email:
        user = User.query.filter_by(email=email).first()

    if user:
        login_user(user, remember=True)
        import uuid
        token_val = uuid.uuid4().hex
        user.session_token = token_val
        db.session.commit()
        session['session_token'] = token_val
        flash('Logged in via Google')
        # if required profile fields missing, send to completion
        if (not user.phone) or str(user.phone).startswith('google_') or not user.flat_number:
            return redirect(url_for('auth.complete_profile'))
        return redirect(url_for('auth.dashboard'))

    # create new user with placeholder phone so DB constraints are satisfied
    import uuid
    placeholder_phone = f'google_{uuid.uuid4().hex[:12]}'

    new_user = User(
        full_name=name,
        email=email,
        phone=placeholder_phone,
        is_admin=False,
        active_plan='No Plan',
        account_status='Active',
        customer_type='Regular'
    )
    new_user.set_password(uuid.uuid4().hex)
    # store picture url temporarily in profile_image (optional)
    if picture:
        try:
            new_user.profile_image = picture
        except Exception:
            pass

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=True)
    token_val = uuid.uuid4().hex
    new_user.session_token = token_val
    db.session.commit()
    session['session_token'] = token_val

    flash('Account created with Google. Please complete your profile.')
    return redirect(url_for('auth.complete_profile'))


# ====================================
# COMPLETE PROFILE AFTER OAUTH
# ====================================


@auth.route('/complete-profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    # only allow if profile incomplete
    if request.method == 'POST':
        phone = request.form.get('phone')
        society = request.form.get('society')
        block = request.form.get('block')
        flat_number = request.form.get('flat_number')

        car_brand = request.form.get('car_brand')
        car_model = request.form.get('car_model')
        car_color = request.form.get('car_color')
        car_registration = request.form.get('car_registration')

        # basic validation
        if not phone:
            flash('Phone is required')
            return redirect(url_for('auth.complete_profile'))

        # check phone uniqueness (ignore own placeholder)
        existing = User.query.filter(User.phone == phone, User.id != current_user.id).first()
        if existing:
            flash('Phone already in use')
            return redirect(url_for('auth.complete_profile'))

        # update user
        current_user.phone = phone
        current_user.society = society
        current_user.block = block
        current_user.flat_number = flat_number
        db.session.commit()

        # create car record if provided
        if car_registration:
            car = Car(
                user_id=current_user.id,
                registration_number=car_registration,
                car_model=car_model,
                car_brand=car_brand,
                car_colour=car_color
            )
            db.session.add(car)
            db.session.commit()

        flash('Profile completed')
        return redirect(url_for('auth.dashboard'))

    # GET -> show completion form only if fields missing
    if current_user.phone and not str(current_user.phone).startswith('google_') and current_user.flat_number:
        return redirect(url_for('auth.dashboard'))

    return render_template('auth/complete_profile.html', user=current_user)


# ====================================
# USER DASHBOARD
# ====================================

@auth.route('/dashboard')
@login_required
def dashboard():

    cars = Car.query.filter_by(
        user_id=current_user.id
    ).all()

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Booking.id.desc()
    ).all()

    active_plan = current_user.active_plan

    return render_template(

        'dashboard/dashboard.html',

        cars=cars,

        bookings=bookings,

        active_plan=active_plan
    )


# ====================================
# OLD SCHEDULE PAGE (DISABLED)
# ====================================

@auth.route(
    '/schedule-old'
)
@login_required
def schedule_old():

    frequencies = Frequency.query.filter_by(
        is_active=True
    ).all()

    plans = Plan.query.filter_by(
        is_active=True
    ).all()

    slots = Slot.query.filter_by(
        is_active=True
    ).all()

    return render_template(

        'booking/schedule.html',

        frequencies=frequencies,

        plans=plans,

        slots=slots
    )




# ====================================
# PLANS PAGE
# ====================================

@auth.route('/plans')
@login_required
def plans():

    # Redirect legacy /plans route to the Tips page (plans template removed)
    return redirect(url_for('plans.tips_page'))


# ====================================
# TRACKING PAGE
# ====================================

@auth.route('/tracking')
@login_required
def tracking():

    booking = Booking.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Booking.id.desc()
    ).first()

    if not booking:

        flash(
            'No Booking Found'
        )

        return redirect(
            url_for(
                'booking.schedule'
            )
        )

    return render_template(

        'tracking/tracking.html',

        booking=booking,

        user=current_user
    )


# ====================================
# PROFILE PAGE
# ====================================

@auth.route('/profile')
@login_required
def profile():

    cars = Car.query.filter_by(
        user_id=current_user.id
    ).all()

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(

        'profile/profile.html',

        user=current_user,

        cars=cars,

        bookings=bookings
    )   


# ====================================
# PAYMENTS PAGE
# ====================================

@auth.route('/payments')
@login_required
def payments():

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(

        'payments/payments.html',

        bookings=bookings
    )


# ====================================
# LOGOUT
# ====================================

@auth.route('/logout')
@login_required
def logout():
    # clear session token so other sessions are invalidated
    try:
        current_user.session_token = None
        db.session.commit()
    except Exception:
        pass

    session.pop('session_token', None)
    logout_user()

    flash('Logged Out Successfully')

    return redirect(url_for('auth.login'))


# ====================================
# ERROR 404
# ====================================

@auth.app_errorhandler(404)
def page_not_found(error):

    return render_template(
        'home/404.html'
    ), 404