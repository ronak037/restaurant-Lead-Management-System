from LMS.db import db
from LMS.models import Leads, Restaurants

from datetime import datetime
from sqlalchemy import CheckConstraint, ForeignKeyConstraint
from sqlalchemy.orm import validates

class Orders(db.Model):
    __tablename__="orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lead_id = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(), default="pending")
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        CheckConstraint(status.in_(['completed', 'placed', 'pending', 'cancelled', 'shipped']), name='order_status_enum'),      
        CheckConstraint(amount>0),
        ForeignKeyConstraint([restaurant_id], [Restaurants.id], ondelete='NO ACTION'),
        ForeignKeyConstraint([lead_id], [Leads.id], ondelete='NO ACTION'),        
    )

    def __repr__(self):
        return f"Order id: {self.id}"

    