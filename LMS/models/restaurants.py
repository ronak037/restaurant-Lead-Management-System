from LMS.db import db

from datetime import datetime
from sqlalchemy import CheckConstraint

class Restaurants(db.Model):
    __tablename__="restaurants"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False, unique=True)
    rating = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(), default="closed")
    created_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        CheckConstraint(status.in_(['open', 'closed', "temp_closed"]), name='restaurant_status_enum'),
        CheckConstraint(rating>=0)
    )

    def __repr__(self):
        return f"Restaurant: {self.name} with id: {self.id}"

