from flask_restx import Namespace, fields

class LeadApi:
    api = Namespace('lead', description="Lead related operations")

    @staticmethod
    def validate_interaction_frequency(value):
        if value is not None and value < 3600*24:
            raise ValueError("Interaction frequency must be more than 1 day")

    @staticmethod
    def validate_status(value):
        valid_statuses = ['new', 'contacted', 'closed', 'converted']
        if value is not None and value not in valid_statuses:
            raise ValueError(f"Lead status must be one of {valid_statuses}")

    lead = api.model('lead', {
        'status': fields.String(required=False, description="lead status", default="new"),
        'interaction_frequency': fields.Integer(required=False, description="lead interaction frequency", default=None),
        'source': fields.String(required=True, description="lead source"),
        'restaurant_id': fields.Integer(required=True, description="restaurant id"),
        'account_username': fields.String(required=True, description="account username")
    })

    lead_patch = api.model('lead_patch', {
        'status': fields.String(required=False, description="lead status", default=None),
        'interaction_frequency': fields.Integer(required=False, description="lead interaction frequency", default=None)    })

class LeadDto:
    def __init__(self, status, interaction_frequency, source, restaurant_id, account_username):
        self.status = status
        self.interaction_frequency = interaction_frequency
        self.source = source
        self.restaurant_id = restaurant_id
        self.account_username = account_username

class LeadAdapter:
    def convert_dict_to_Dto(self, data: dict):
        return LeadDto(data['status'], data['interaction_frequency'], data['source'], data['restaurant_id'], data['account_username'])

    def convert_to_dict(self, data: LeadDto):
        return {
            'status': data.status,
            'interaction_frequency': data.interaction_frequency,
            'source': data.source,
            'restaurant_id': data.restaurant_id,
            'account_username': data.account_username
        }

    def convert_db_object_to_Dto(self, db_object):
        return LeadDto(db_object.status, db_object.interaction_frequency, db_object.source, db_object.restaurant_id, db_object.account_username)


class LeadPatchDto:
    def __init__(self, status, interaction_frequency):
        self.status = status
        self.interaction_frequency = interaction_frequency

class LeadPatchAdapter:
    def convert_dict_to_Dto(self, data: dict):
        return LeadPatchDto(data.get('status', None), data.get('interaction_frequency', None),)

    def convert_to_dict(self, data: LeadPatchDto):
        return {
            'status': data.status,
            'interaction_frequency': data.interaction_frequency
        }


class LeadInteractionInfoDto:
    def __init__(self, lead_id, status, interaction_frequency, source, restaurant_id, account_username, interaction_id, latest_interaction_time):
        self.lead_id = lead_id
        self.status = status
        self.interaction_frequency = interaction_frequency
        self.source = source
        self.restaurant_id = restaurant_id
        self.account_username = account_username
        self.interaction_id = interaction_id
        self.latest_interaction_time = latest_interaction_time

class LeadInteractionInfoAdapter:
    def convert_dict_to_Dto(self, data: dict):
        return LeadInteractionInfoDto(data['lead_id'], data['status'], data['interaction_frequency'], data['source'], 
                                data['restaurant_id'], data['account_username'], data['interaction_id'], data['latest_interaction_time'])

    def convert_to_dict(self, data: LeadInteractionInfoDto):
        return {
            'lead_id': data.lead_id,
            'lead_status': data.status,
            'interaction_frequency': data.interaction_frequency,
            'lead_source': data.source,
            'restaurant_id': data.restaurant_id,
            'account_username': data.account_username,
            'interaction_id': data.interaction_id,
            'latest_interaction_time': data.latest_interaction_time.strftime('%Y-%m-%d %H:%M:%S')
        }

    def convert_db_object_to_Dto(self, db_object):
        return LeadInteractionInfoDto(db_object.lead_id, db_object.lead_status, db_object.interaction_frequency, 
                                    db_object.lead_source, db_object.restaurant_id, db_object.account_username,
                                    db_object.interaction_id, db_object.latest_interaction_time)

