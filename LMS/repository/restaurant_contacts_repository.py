from LMS.db import db
from LMS.models import RestaurantContacts
from LMS.entities import RestaurantContactAdapter
from LMS.exceptions import RestaurantContactExistsException

class RestaurantContactsRepository:
    def __init__(self):
        self.restaurant_contact_adapter = RestaurantContactAdapter()

    def add_restaurant_contact(self, restaurant_contact_dto):
        db_contact = RestaurantContacts.query.filter(RestaurantContacts.phone_number==restaurant_contact_dto.phone_number).first()

        if not db_contact:
            restaurant_contact = RestaurantContacts(
                name = restaurant_contact_dto.name,
                role = restaurant_contact_dto.role,
                phone_number = restaurant_contact_dto.phone_number,
                restaurant_id = restaurant_contact_dto.restaurant_id
            )
            self.save_db(restaurant_contact)
        else:
            raise RestaurantContactExistsException
            
    def get_restaurant_contact(self, id):
        db_restaurant_contact = RestaurantContacts.query.filter_by(id=id).first()
        if db_restaurant_contact is None:
            return None
        # convert to dto
        restaurant_contact_dto = self.restaurant_contact_adapter.convert_db_object_to_Dto(db_restaurant_contact)
        return restaurant_contact_dto

    def save_db(self, data):
        db.session.add(data)
        db.session.commit()
