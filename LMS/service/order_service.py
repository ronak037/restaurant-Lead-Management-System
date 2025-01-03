from LMS.repository import OrderRepository
from LMS.utils import Singleton
from LMS.entities import OrderAdapter, OrderFilterAdapter, OrderDto, LeadAdapter
from LMS.service import RestaurantService, LeadService
from LMS.exceptions import RestaurantNotExistsException, LeadNotExistsException

class OrderService(metaclass=Singleton):
    def __init__(self):
        self.order_repo = OrderRepository()
        self.order_adapter = OrderAdapter()
        self.order_filter_adapter = OrderFilterAdapter()
        self.lead_adapter = LeadAdapter()
        self.restaurant_service = RestaurantService()
        self.lead_service = LeadService()

    def add_order(self, order_dict: dict):
        order_dto = self.order_adapter.convert_dict_to_Dto(order_dict)

        # check if restaurant_id exists in restaurants table
        restaurant_id = order_dto.restaurant_id
        if self.restaurant_service.get_restaurant(restaurant_id) is None:
            raise RestaurantNotExistsException("Restaurant does not exist, so cannot add order")
        
        # check if lead_id exists in leads table
        lead_id = order_dto.lead_id
        lead_dict = self.lead_service.get_lead(lead_id)
        if lead_dict is None:
            raise LeadNotExistsException("Lead does not exist, so cannot add order")
        
        if lead_dict['status'] != 'converted':
            raise LeadNotExistsException("Lead not yet converted")

        # check if restaurant id is matching with restarant id in lead
        lead_obj = self.lead_adapter.convert_dict_to_Dto(lead_dict)
        if lead_obj.restaurant_id != restaurant_id:
            raise RestaurantNotExistsException("Restaurant id does not match with restaurant id in lead")

        self.order_repo.add_order(order_dto)

    def get_orders(self, filter_condition):
        filter_dto = self.order_filter_adapter.convert_dict_to_Dto(filter_condition)
        order_dto_list = self.order_repo.get_filtered_orders(filter_dto)
        order_dict_list = []
        for order_dto in order_dto_list:
            order_dict_list.append(self.order_adapter.convert_to_dict(order_dto))
        return order_dict_list
    
    def get_order(self, order_id) -> OrderDto:
        order_dto = self.order_repo.get_order(order_id)
        return self.order_adapter.convert_to_dict(order_dto) if order_dto else None
