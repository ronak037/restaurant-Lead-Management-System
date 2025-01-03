from LMS.repository import RestaurantContactsRepository
from LMS.utils import Singleton
from LMS.entities import RestaurantContactAdapter, RestaurantContactDto
from LMS.service import RestaurantService
from LMS.exceptions import RestaurantNotExistsException

class RestaurantContactService(metaclass=Singleton):
    def __init__(self):
        self.restaurant_contact_repo = RestaurantContactsRepository()
        self.restaurant_contact_adapter = RestaurantContactAdapter()
        self.restaurant_service = RestaurantService()
        
    def add_restaurant_contact(self, restaurant_contact: dict):
        restaurant_contact_dto = self.restaurant_contact_adapter.convert_dict_to_Dto(restaurant_contact)
        
        # check if restaurant_id exists in restaurants table
        restaurant_id = restaurant_contact_dto.restaurant_id
        if self.restaurant_service.get_restaurant(restaurant_id) is None:
            raise RestaurantNotExistsException("Restaurant does not exist, so cannot add contact")
        
        self.restaurant_contact_repo.add_restaurant_contact(restaurant_contact_dto)
    
    def get_restaurant_contact(self, restaurant_contact_id) -> RestaurantContactDto:
        restaurant_contact_dto = self.restaurant_contact_repo.get_restaurant_contact(restaurant_contact_id)
        return self.restaurant_contact_adapter.convert_to_dict(restaurant_contact_dto) if restaurant_contact_dto else None
