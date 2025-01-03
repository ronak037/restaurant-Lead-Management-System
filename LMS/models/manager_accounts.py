from LMS.db import db

# from sqlalchemy import Column
from datetime import datetime

class ManagerAccounts(db.Model):
    __tablename__ = "manager_accounts"

    username = db.Column(db.String(), 
                         unique=True, 
                         primary_key=True)
    password = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(), default="active")
    role = db.Column(db.String(), default="employee")
    created_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        db.CheckConstraint(role.in_(['employee', 'admin']), name='acc_role_enum'),
        db.CheckConstraint(status.in_(['active', 'inactive', 'suspended']), name='acc_status_enum')
    )
    
    def __repr__(self):
        return f"Account username: {self.username}"
