from LMS.repository import LeadRepository
from LMS.utils import Singleton
from LMS.entities import LeadAdapter, LeadPatchAdapter, LeadInteractionInfoAdapter
from LMS.service import RestaurantService, ManagerAccountService
from LMS.exceptions import RestaurantNotExistsException, ManagerAccountNotExistsException,\
                        LeadExistsException, LeadNotExistsException, AuthenticationException

from datetime import datetime

class LeadService(metaclass=Singleton):
    def __init__(self):
        self.lead_repo = LeadRepository()
        self.lead_adapter = LeadAdapter()
        self.lead_interaction_info_adapter = LeadInteractionInfoAdapter()
        self.update_lead_adapter= LeadPatchAdapter()
        self.restaurant_service = RestaurantService()
        self.manager_account_service = ManagerAccountService()
    
    def add_lead(self, lead_dict: dict):
        lead_dto = self.lead_adapter.convert_dict_to_Dto(lead_dict)

        # check if restaurant_id exists in restaurants table
        restaurant_id = lead_dto.restaurant_id
        if self.restaurant_service.get_restaurant(restaurant_id) is None:
            raise RestaurantNotExistsException("Restaurant does not exist, so cannot add lead")
        
        # check if account_username exists in restaurants table
        account_username = lead_dto.account_username
        if self.manager_account_service.get_manager_account(account_username) is None:
            raise ManagerAccountNotExistsException("Manager account does not exist, so cannot add lead")

        self.lead_repo.add_lead(lead_dto)

    def get_lead(self, lead_id, current_user=None):
        lead_dto = self.lead_repo.get_lead(lead_id)
        if current_user and current_user['role']!='admin' and lead_dto.account_username != current_user['username']:
            raise AuthenticationException("You are not authorized to view this lead")
        return self.lead_adapter.convert_to_dict(lead_dto) if lead_dto else None

    def update_lead(self, lead_id: str, data: dict, current_user=None):
        update_lead_dto = self.update_lead_adapter.convert_dict_to_Dto(data)

        # check if all attributes are None
        update_lead_dto_attributes = vars(update_lead_dto)
        if all(value is None for value in update_lead_dto_attributes.values()):
            raise ValueError("Atleast one attribute must be passed to update the lead")

        db_lead_dict = self.get_lead(lead_id)
        if current_user and current_user['role']!='admin' and db_lead_dict['account_username'] != current_user['username']:
            raise AuthenticationException("You are not authorized to update this lead")

        if db_lead_dict['status'] in ['converted', 'closed']:
            raise LeadExistsException("Lead is closed or converted successfully, can't change now")

        lead_dto = self.lead_repo.update_lead(lead_id, update_lead_dto)
        return self.lead_adapter.convert_to_dict(lead_dto)

    def find_leads_requiring_call_today(self, current_user=None):
        query = self.lead_repo.get_latest_interaction()
        today = datetime.now()
        leads_requiring_call = []

        for result in query:
            if current_user and current_user['role']!='admin' and result.account_username!=current_user['username']:
                continue
            lead_id = result.lead_id
            interaction_freq = result.interaction_frequency
            last_interaction_time = result.latest_interaction_time

            # Check if the last interaction time is None (i.e., never had an interaction so add it)
            if last_interaction_time is None:
                leads_requiring_call.append(lead_id)
            elif interaction_freq is None:
                continue
            else:
                time_diff = today - last_interaction_time
                if time_diff.total_seconds() >= interaction_freq:
                    lead_interaction_dict = self.lead_interaction_info_adapter.convert_to_dict(result)
                    leads_requiring_call.append(lead_interaction_dict)

        return leads_requiring_call
