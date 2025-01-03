from flask import request
from flask_restx import Resource

from LMS.exceptions import RestaurantContactExistsException, RestaurantNotExistsException
from LMS.entities import RestaurantContactApi
from LMS.service import RestaurantContactService
from LMS.utils import authentication

api = RestaurantContactApi.api
_restaurant_contact = RestaurantContactApi.restaurant_contact
restaurant_contact_service = RestaurantContactService()

@api.route('/')
class RestaurantContactList(Resource):
    @api.doc('Add new restaurant contact', params={
            'x-access-tokens': {
                'description': 'Bearer token for authentication',
                'in': 'header',
                'type': 'string',
            }
        })
    @api.expect(_restaurant_contact, validate=True)
    @authentication.token_required()
    def post(_, self):
        data = request.json

        # payload validations
        try:
            RestaurantContactApi.validate_phone_number(data['phone_number'])
            RestaurantContactApi.validate_role(data['role'])
        except ValueError as e:
            res_obj = {
                'status': 'failure',
                'message': str(e)
            }
            return res_obj, 400

        try:
            restaurant_contact_service.add_restaurant_contact(data)
            res_obj = {
                'status': 'success',
                'message': 'Restaurant contact added successfully'
            }
            return res_obj, 201
        except RestaurantContactExistsException:
            res_obj = {
                'status': 'failure',
                'message': "Restaurant contact already exists"
            }
            return res_obj, 409
        except RestaurantNotExistsException:
            res_obj = {
                'status': 'failure',
                'message': 'Restaurant does not exist, send correct restaurant id'
            }
            return res_obj, 400
        except Exception:
            res_obj = {
                'status': 'failure',
                'message': 'Internal server error'
            }
            return res_obj, 500

@api.route('/<restaurant_contact_id>')
@api.param('restaurant_contact_id', 'Restaurant contact identifier')
class RestaurantContact(Resource):
    @api.doc('get a restaurant contact', params={
            'x-access-tokens': {
                'description': 'Bearer token for authentication',
                'in': 'header',
                'type': 'string',
            }
        })
    @authentication.token_required()
    def get(_, self, restaurant_contact_id):
        restaurant_contact = restaurant_contact_service.get_restaurant_contact(restaurant_contact_id)
        if restaurant_contact is None:
            res_obj = {'status': 'failure', 'message': 'Restaurant contact not found'}
            return res_obj, 404
        else:
            res_obj = {'status': 'success', 'data': restaurant_contact}
            return res_obj, 200
