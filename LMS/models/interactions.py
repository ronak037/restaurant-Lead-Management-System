from LMS.db import db
from LMS.models import Leads, ManagerAccounts

from datetime import datetime
from sqlalchemy import CheckConstraint, ForeignKeyConstraint

class Interactions(db.Model):
    __tablename__="interactions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(), default="in_progress")
    lead_id = db.Column(db.Integer, nullable=False)
    account_username = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    notes = db.Column(db.String())

    __table_args__ = (
        CheckConstraint(status.in_(['in_progress', 'completed', 'missed', 'rescheduled']), name='interaction_status_enum'),      
        ForeignKeyConstraint([lead_id], [Leads.id], ondelete='NO ACTION'),        
        ForeignKeyConstraint([account_username], [ManagerAccounts.username], ondelete='NO ACTION'),        
    )

    def __repr__(self):
        return f"Interaction id: {self.id}"

    