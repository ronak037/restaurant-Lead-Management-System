import traceback

from flask import request
from flask_restx import Resource

from LMS.entities import InteractionApi
from LMS.service import InteractionService
from LMS.exceptions import LeadNotExistsException, ManagerAccountNotExistsException, LeadExistsException
from LMS.utils import authentication

api = InteractionApi.api
_interaction = InteractionApi.interaction
interaction_service = InteractionService()

@api.route('/')
class InteractionList(Resource):
    @api.doc('Add new interaction', params={
            'x-access-tokens': {
                'description': 'Bearer token for authentication',
                'in': 'header',
                'type': 'string',
            }
        })
    @api.expect(_interaction, validate=True)
    @authentication.token_required()
    def post(_, self):
        data = request.json
        if data.get('status', None) is None:
            data['status'] = "in_progress"
        if data.get('notes', None) is None:
            data['notes'] = None

        # payload validations
        try:
            InteractionApi.validate_status(data['status'])
        except ValueError as e:
            res_obj = {
                'status': 'failure',
                'message': str(e)
            }
            return res_obj, 400
        
        try:
            interaction_service.add_interaction(data)
            res_obj = {
                'status': 'success',
                'message': 'Interaction added successfully'
            }
            return res_obj, 201
        except (LeadNotExistsException, ManagerAccountNotExistsException, LeadExistsException) as e:
            res_obj = {
                'status': 'failure',
                'message': str(e)
            }
            return res_obj, 409
        except Exception:
            print(traceback.format_exc())
            res_obj = {
                'status': 'failure',
                'message': 'Internal server error'
            }
            return res_obj, 500

@api.route('/<interaction_id>')
@api.param('interaction_id', 'Interaction identifier')
class Interaction(Resource):
    @api.doc('get an interaction', params={
            'x-access-tokens': {
                'description': 'Bearer token for authentication',
                'in': 'header',
                'type': 'string',
            }
        })
    @authentication.token_required()
    def get(_, self, interaction_id):
        interaction = interaction_service.get_interaction(interaction_id)
        if interaction is None:
            res_obj = {'status': 'failure', 'message': 'Interaction not found'}
            return res_obj, 404
        else:
            res_obj = {'status': 'success', 'data': interaction}
            return res_obj, 200
