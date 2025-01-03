from LMS.repository import InteractionRepository
from LMS.utils import Singleton
from LMS.entities import InteractionAdapter, InteractionDto, LeadAdapter
from LMS.service import LeadService, ManagerAccountService
from LMS.exceptions import LeadNotExistsException, ManagerAccountNotExistsException

class InteractionService(metaclass=Singleton):
    def __init__(self):
        self.interaction_repo = InteractionRepository()
        self.interaction_adapter = InteractionAdapter()
        self.lead_service = LeadService()
        self.lead_adapter = LeadAdapter()
        self.manager_account_service = ManagerAccountService()

    def add_interaction(self, interaction_dict: dict):
        interaction_dto = self.interaction_adapter.convert_dict_to_Dto(interaction_dict)

        # check if account_username exists in restaurants table
        account_username = interaction_dto.account_username
        if self.manager_account_service.get_manager_account(account_username) is None:
            raise ManagerAccountNotExistsException("Manager account does not exist, so can't take order")

        # check if lead_id exists in leads table
        lead_id = interaction_dto.lead_id
        lead_dict = self.lead_service.get_lead(lead_id)
        if lead_dict is None:
            raise LeadNotExistsException("Lead does not exist, so can't take order")

        # update status of lead to contacted
        self.lead_service.update_lead(lead_id, {'status': 'contacted'})
        
        self.interaction_repo.add_interaction(interaction_dto)

    def get_interaction(self, interaction_id) ->InteractionDto:
        interaction_dto = self.interaction_repo.get_interaction(interaction_id)
        return self.interaction_adapter.convert_to_dict(interaction_dto) if interaction_dto else None
