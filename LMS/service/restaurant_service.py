from LMS.repository import RestaurantRepository
from LMS.utils import Singleton
from LMS.entities import RestaurantAdapter, RestaurantDto

class RestaurantService(metaclass=Singleton):
    def __init__(self):
        self.restaurant_repo = RestaurantRepository()
        self.restaurant_adapter = RestaurantAdapter()

    def add_restaurant(self, restaurant: dict):
        restaurant_dto = self.restaurant_adapter.convert_dict_to_Dto(restaurant)
        self.restaurant_repo.add_restaurant(restaurant_dto)

    def get_restaurant(self, restaurant_id) -> RestaurantDto:
        restaurant_dto = self.restaurant_repo.get_restaurant(restaurant_id)
        return self.restaurant_adapter.convert_to_dict(restaurant_dto) if restaurant_dto else None
