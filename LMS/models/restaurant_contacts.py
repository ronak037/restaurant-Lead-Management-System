from LMS.db import db
from LMS.models import Restaurants

from sqlalchemy import CheckConstraint, ForeignKeyConstraint

class RestaurantContacts(db.Model):
    __tablename__="restaurant_contacts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    restaurant_id = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        CheckConstraint(role.in_(['manager', 'supervisor', 'contractor']), name='contact_role_enum'),      
        ForeignKeyConstraint([restaurant_id], [Restaurants.id], ondelete='NO ACTION'),
        CheckConstraint("length(phone_number) = 10 AND phone_number ~ '^[0-9]+$'", name='phone_number_only_digits')
    )

    def __repr__(self):
        return f"Contact name: {self.name}"
