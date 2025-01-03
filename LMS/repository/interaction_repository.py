from LMS.db import db
from LMS.models import Interactions
from LMS.entities import InteractionAdapter, InteractionDto

class InteractionRepository:
    def __init__(self):
        self.interaction_adapter = InteractionAdapter()

    def add_interaction(self, interaction_dto: InteractionDto):
        interaction = Interactions(
            status = interaction_dto.status,
            lead_id = interaction_dto.lead_id,
            account_username = interaction_dto.account_username,
            notes = interaction_dto.notes
        )
        self.save_db(interaction)
    
    def get_interaction(self, id):
        db_interaction = Interactions.query.filter_by(id=id).first()
        if db_interaction is None:
            return None
        # convert to dto
        interaction_dto = self.interaction_adapter.convert_db_object_to_Dto(db_interaction)
        return interaction_dto

    def save_db(self, data):
        db.session.add(data)
        db.session.commit()
