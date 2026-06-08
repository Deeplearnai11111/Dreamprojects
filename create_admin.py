from app import create_app, db
from app.models.user import User
import os
import secrets

app = create_app()

with app.app_context():
    admin = User.query.filter_by(phone='admin').first()

    env_pass = os.environ.get('ADMIN_PASSWORD')
    if env_pass:
        password_to_set = env_pass
    else:
        password_to_set = secrets.token_urlsafe(12)

    if not admin:
        admin = User(
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
        db.session.add(admin)

    admin.set_password(password_to_set)
    db.session.commit()

    print('Admin ready:', admin.id, admin.full_name, admin.phone, admin.email)
    if not env_pass:
        print('Generated admin password (store securely):', password_to_set)
