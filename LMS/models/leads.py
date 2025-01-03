from LMS.db import db
from LMS.models import Restaurants, ManagerAccounts

from datetime import datetime
from sqlalchemy import CheckConstraint, ForeignKeyConstraint, UniqueConstraint, or_

class Leads(db.Model):
    __tablename__="leads"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(), default="new")
    interaction_frequency = db.Column(db.Integer)
    source = db.Column(db.String(), nullable=False)
    restaurant_id = db.Column(db.Integer, nullable=False)
    account_username = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        CheckConstraint(status.in_(['new', 'contacted', 'closed', 'converted']), name='lead_status_enum'),      
        CheckConstraint(
            or_(
                interaction_frequency.is_(None),  # Allow interaction_frequency to be NULL
                interaction_frequency > 3600 * 24    # Enforce check only if not NULL
            ),
            name='lead_interaction_frequency_check'
        ),
        CheckConstraint(source.isnot(None), name='lead_source_not_null'),
        ForeignKeyConstraint([restaurant_id], [Restaurants.id], ondelete='NO ACTION'),        
        ForeignKeyConstraint([account_username], [ManagerAccounts.username], ondelete='NO ACTION'),
        UniqueConstraint('source', 'restaurant_id', name='unique_source_restaurant')  # Enforce uniqueness for source + restaurant_id
    )

    def __repr__(self):
        return f"Lead id: {self.id}"

    
