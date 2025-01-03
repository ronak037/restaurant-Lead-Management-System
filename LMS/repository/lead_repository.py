from LMS.db import db
from LMS.models import Leads, Interactions
from LMS.entities import LeadAdapter, LeadInteractionInfoAdapter
from LMS.exceptions import LeadExistsException, LeadNotExistsException

from sqlalchemy.orm import aliased

class LeadRepository:
    def __init__(self):
        self.lead_adapter = LeadAdapter()
        self.lead_interaction_info_adapter = LeadInteractionInfoAdapter()

    def add_lead(self, lead_dto):
        db_lead = Leads.query.filter(Leads.source==lead_dto.source, 
                                     Leads.restaurant_id==lead_dto.restaurant_id).first()

        if not db_lead:
            lead = Leads(
                status = lead_dto.status,
                interaction_frequency = lead_dto.interaction_frequency,
                source = lead_dto.source,
                restaurant_id = lead_dto.restaurant_id,
                account_username = lead_dto.account_username
            )
            self.save_db(lead)
        else:
            raise LeadExistsException

    def get_lead(self, id):
        db_lead = Leads.query.filter_by(id=id).first()
        if db_lead is None:
            return None
        # convert to dto
        lead_dto = self.lead_adapter.convert_db_object_to_Dto(db_lead)
        return lead_dto

    def update_lead(self, lead_id, update_lead_dto):
        db_lead = Leads.query.filter(Leads.id==lead_id).first()
        if not db_lead:
            raise LeadNotExistsException("Lead does not exists")
        
        dto_attributes = vars(update_lead_dto)
        for key, value in dto_attributes.items():
            if value is not None:
                setattr(db_lead, key, value)
        self.commit_db()

        #convert to dto
        lead_dto = self.lead_adapter.convert_db_object_to_Dto(db_lead)
        return lead_dto

    def get_latest_interaction(self):
        # Subquery to get the latest interaction time and interaction id for each lead
        latest_interaction_subquery = db.session.query(
            Interactions.lead_id,
            db.func.max(Interactions.created_at).label('latest_interaction_time')  # Get the most recent interaction time
        ).group_by(Interactions.lead_id).subquery()

        query = db.session.query(
                        Leads.id.label('lead_id'),
                        Interactions.id.label('interaction_id'),
                        Leads.interaction_frequency,
                        Leads.status.label('lead_status'),
                        Leads.source.label('lead_source'),
                        Leads.restaurant_id,
                        Leads.account_username,
                        latest_interaction_subquery.c.latest_interaction_time,
                    ).join(
                        latest_interaction_subquery,
                        latest_interaction_subquery.c.lead_id == Leads.id
                    ).join(
                        Interactions,
                        (Interactions.lead_id == latest_interaction_subquery.c.lead_id) &
                        (Interactions.created_at == latest_interaction_subquery.c.latest_interaction_time)  # Join on the latest interaction time
                    ).all()
        
        result = []
        for q in query:
            result.append(self.lead_interaction_info_adapter.convert_db_object_to_Dto(q))
        return result


    def commit_db(self):
        db.session.commit()
    
    def save_db(self, data):
        db.session.add(data)
        self.commit_db()
