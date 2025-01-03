from LMS.db import db
from LMS.models import Restaurants
from LMS.entities import RestaurantAdapter
from LMS.exceptions import RestaurantExistsException

class RestaurantRepository:
    def __init__(self):
        self.restaurant_adapter = RestaurantAdapter()

    def add_restaurant(self, restaurant_dto):
        db_restaurant = Restaurants.query.filter(Restaurants.location==restaurant_dto.location).first()
        if not db_restaurant:
            new_restaurant = Restaurants(
                name = restaurant_dto.name,
                location = restaurant_dto.location,
            )
            self.save_db(new_restaurant)
        else:
            raise RestaurantExistsException

    def get_restaurant(self, id):
        db_restaurant = Restaurants.query.filter_by(id=id).first()        
        if db_restaurant is None:
            return None
        # convert to dto
        restaurant_dto = self.restaurant_adapter.convert_db_object_to_Dto(db_restaurant)
        return restaurant_dto

    def save_db(self, data):
        db.session.add(data)
        db.session.commit()
