from app import db


class AuditLog(db.Model):

    __tablename__ = 'audit_logs'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    actor = db.Column(
        db.String(255)
    )

    action = db.Column(
        db.String(255)
    )

    details = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
