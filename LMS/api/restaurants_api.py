from flask import request
from flask_restx import Resource

from LMS.exceptions import RestaurantExistsException
from LMS.entities import RestaurantApi
from LMS.service import RestaurantService
from LMS.utils import authentication

api = RestaurantApi.api
_restaurant = RestaurantApi.restaurant
restaurant_service = RestaurantService()

# token_parser = RestaurantApi.headers

@api.route('/')
class RestaurantList(Resource):
    @api.doc('Add new restaurant', params={
            'x-access-tokens': {
                'description': 'Bearer token for authentication',
                'in': 'header',
                'type': 'string',
            }
        })
    @api.expect(_restaurant, validate=True)
    @authentication.admin_token_required()
    def post(_, self):
        data = request.json
        try:
            restaurant_service.add_restaurant(data)
            res_obj = {
                'status': 'success',
                'message': 'Restaurant added successfully'
            }
            return res_obj, 201
        except RestaurantExistsException as e:
            res_obj = {
                'status': 'failure',
                'message': "Reastaurant already exists"
            }
            return res_obj, 409
        except Exception:
            res_obj = {
                'status': 'failure',
                'message': 'Internal server error'
            }
            return res_obj, 500


@api.route('/<int:restaurant_id>')
@api.param('restaurant_id', 'Restaurant identifier')
class Restaurant(Resource):
    @authentication.token_required()
    @api.doc('get a restaurant', params={
            'x-access-tokens': {
                'description': 'Bearer token for authentication',
                'in': 'header',
                'type': 'string',
            }
        })
    def get(_, self, restaurant_id):
        restaurant = restaurant_service.get_restaurant(restaurant_id)
        if restaurant is None:
            res_obj = {'status': 'failure', 'message': 'Restaurant not found'}
            return res_obj, 404
        else:
            res_obj = {'status': 'success', 'data': restaurant}
            return res_obj, 200
