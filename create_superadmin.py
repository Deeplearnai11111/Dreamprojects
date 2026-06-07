from app import create_app, db
from app.models.user import User
import os
import secrets

app = create_app()

with app.app_context():
    u = User.query.filter_by(phone='superadmin').first()

    if not u:
        u = User(
            full_name='Super Admin',
            phone='superadmin',
            email='super@cleanzo.in',
            society='CLEANZO HQ',
            block='ADMIN',
            flat_number='000',
            is_admin=True,
            role='super_admin',
            active_plan='ADMIN',
            account_status='Active',
            customer_type='Administrator'
        )
        db.session.add(u)

    # set or reset password from environment variable if provided
    env_pass = os.environ.get('SUPERADMIN_PASSWORD')
    if env_pass:
        password_to_set = env_pass
    else:
        # generate a secure random password and print it so operator can record it
        password_to_set = secrets.token_urlsafe(16)

    u.set_password(password_to_set)

    db.session.commit()

    print('Super admin ready:', u.id, u.full_name, u.phone, u.email)
    if not env_pass:
        print('Generated superadmin password (store this securely):', password_to_set)
