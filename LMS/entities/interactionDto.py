from flask_restx import Namespace, fields

class InteractionApi:
    api = Namespace('interaction', description="Interaction related operations")

    @staticmethod
    def validate_status(value):
        valid_statuses = ['in_progress', 'completed', 'missed', 'rescheduled']
        if value is not None and value not in valid_statuses:
            raise ValueError(f"Interaction status must be one of {valid_statuses}")

    interaction = api.model('interaction', {
        'status': fields.String(required=False, description="interaction status", default="in_progress"),
        'lead_id': fields.Integer(required=True, description="lead id"),
        'account_username': fields.String(required=True, description="account username"),
        'notes': fields.String(required=False, description="call notes")
    })

class InteractionDto:
    def __init__(self, status, lead_id, account_username, notes):
        self.status = status
        self.lead_id = lead_id
        self.account_username = account_username
        self.notes = notes

class InteractionAdapter:
    def convert_dict_to_Dto(self, data: dict):
        return InteractionDto(data['status'], data['lead_id'], data['account_username'], data['notes'])

    def convert_to_dict(self, data: InteractionDto):
        return {
            'status': data.status,
            'lead_id': data.lead_id,
            'account_username': data.account_username,
            'notes': data.notes
        }

    def convert_db_object_to_Dto(self, db_object):
        return InteractionDto(db_object.status, db_object.lead_id, db_object.account_username, db_object.notes)
