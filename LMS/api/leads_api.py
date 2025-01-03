import traceback

from flask import request
from flask_restx import Resource

from LMS.exceptions import LeadExistsException, LeadNotExistsException, RestaurantNotExistsException,\
                        ManagerAccountNotExistsException, AuthenticationException
from LMS.entities import LeadApi
from LMS.service import LeadService
from LMS.utils import authentication

api = LeadApi.api
_lead = LeadApi.lead
_lead_update = LeadApi.lead_patch
lead_service = LeadService()

@api.route('/')
class LeadList(Resource):
    @api.doc('Add new lead', params={
            'x-access-tokens': {
                'description': 'Bearer token for authentication',
                'in': 'header',
                'type': 'string',
            }
        })
    @api.expect(_lead, validate=True)
    @authentication.token_required()
    def post(_, self):
        data = request.json
        if data.get('status', None) is None:
            data['status'] = 'new'
        if data.get('interaction_frequency', None) is None:
            data['interaction_frequency'] = None

        # payload validations
        try:
            LeadApi.validate_status(data['status'])
            LeadApi.validate_interaction_frequency(data['interaction_frequency'])
        except ValueError as e:
            res_obj = {
                'status': 'failure',
                'message': str(e)
            }
            return res_obj, 400

        try:
            lead_service.add_lead(data)
            res_obj = {
                'status': 'success',
                'message': 'Lead added successfully'
            }
            return res_obj, 201
        except LeadExistsException:
            res_obj = {
                'status': 'failure',
                'message': 'Lead already exists'
            }
            return res_obj, 409
        except RestaurantNotExistsException:
            res_obj = {
                'status': 'failure',
                'message': 'Restaurant does not exist, send correct restaurant id'
            }
            return res_obj, 400
        except ManagerAccountNotExistsException:
            res_obj = {
                'status': 'failure',
                'message': 'Manager account does not exist, send correct manager account id'
            }
            return res_obj, 400
        except Exception:
            print(traceback.format_exc())
            res_obj = {
                'status': 'failure',
                'message': 'Internal server error'
            }
            return res_obj, 500


@api.route('/<int:lead_id>')
@api.param('lead_id', 'Lead identifier')
class Lead(Resource):
    @api.doc('get a lead', params={
            'x-access-tokens': {
                'description': 'Bearer token for authentication',
                'in': 'header',
                'type': 'string',
            }
        })
    @authentication.token_required()
    def get(current_user, self, lead_id):
        try:
            lead = lead_service.get_lead(lead_id, current_user)
            if lead is None:
                res_obj = {'status': 'failure', 'message': 'Lead not found'}
                return res_obj, 404
            else:
                res_obj = {'status': 'success', 'data': lead}
                return res_obj, 200
        except AuthenticationException as e:
            res_obj = {
                'status': 'failure',
                'message': str(e)
            }
            return res_obj, 401
        except Exception:
            print(traceback.format_exc())
            res_obj = {
                'status': 'failure',
                'message': 'Internal server error'
            }
            return res_obj, 500


@api.route('/<int:lead_id>/status')
@api.param('lead_id', 'Lead identifier to get status')
class LeadStatus(Resource):
    @api.doc('get lead status', params={
            'x-access-tokens': {
                'description': 'Bearer token for authentication',
                'in': 'header',
                'type': 'string',
            }
        })
    @authentication.token_required()
    def get(current_user, self, lead_id):
        try:
            lead = lead_service.get_lead(lead_id, current_user)
            if lead is None:
                res_obj = {'status': 'failure', 'message': 'Lead not found'}
                return res_obj, 404
            else:
                res_obj = {'status': 'success', 'data': {'lead_status': lead['status']}}
                return res_obj, 200
        except AuthenticationException as e:
            res_obj = {
                'status': 'failure',
                'message': str(e)
            }
            return res_obj, 401
        except Exception:
            print(traceback.format_exc())
            res_obj = {
                'status': 'failure',
                'message': 'Internal server error'
            }
            return res_obj, 500



@api.route('/<int:lead_id>/interaction_freq')
@api.param('lead_id', 'lead identifier to do operations on Interaction frequency')
class LeadInteractionFreq(Resource):
    @api.doc('update interaction frequency', params={
            'x-access-tokens': {
                'description': 'Bearer token for authentication',
                'in': 'header',
                'type': 'string',
            }
        })
    @api.expect(_lead_update, validate=True)
    @authentication.token_required()
    def patch(current_user, self, lead_id):
        data = request.json

        try:
            if 'interaction_frequency' not in data.keys():
                raise ValueError("Expecting interaction_frequency key in payload")
            LeadApi.validate_interaction_frequency(data['interaction_frequency'])
        except ValueError as e:
            res_obj = {
                'status': 'failure',
                'message': str(e)
            }
            return res_obj, 400

        try:
            lead = lead_service.update_lead(lead_id, data, current_user)
            res_obj = {'status': 'success', 'data': lead}
            return res_obj, 200
        except (ValueError, LeadNotExistsException) as e:
            res_obj = {
                'status': 'failure',
                'message': str(e)
            }
            return res_obj, 400
        except Exception:
            print(traceback.format_exc())
            res_obj = {
                'status': 'failure',
                'message': 'Internal server error'
            }
            return res_obj, 500


@api.route('/pending_interactions')
class DailyLeads(Resource):
    @api.doc('get leads to call today', params={
            'x-access-tokens': {
                'description': 'Bearer token for authentication',
                'in': 'header',
                'type': 'string',
            }
        })
    @authentication.token_required(raise_exception=False)
    def get(current_user, self):
        try:
            leads = lead_service.find_leads_requiring_call_today(current_user)
            res_obj = {
                'status': 'success',
                'data': {
                    'leads': leads
                }
            }
            return res_obj, 200
        except Exception:
            print(traceback.format_exc())
            res_obj = {
                'status': 'failure',
                'message': 'Internal server error'
            }
            return res_obj, 500
