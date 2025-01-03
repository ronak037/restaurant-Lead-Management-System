import traceback

from datetime import datetime
from flask import request
from flask_restx import Resource, reqparse

from LMS.exceptions import LeadNotExistsException, RestaurantNotExistsException
from LMS.entities import OrderApi
from LMS.service import OrderService
from LMS.utils import authentication

api = OrderApi.api
_order = OrderApi.order
order_service = OrderService()

parser = reqparse.RequestParser()
parser.add_argument("order_id", type=int, action="split")
parser.add_argument("lead_id", type=int, action="split")
parser.add_argument("restaurant_id", type=int, action="split")
parser.add_argument("amount", type=float, action="split")
parser.add_argument("status", type=str, action="split")
parser.add_argument("from_date", type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'))
parser.add_argument("to_date", type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'))

@api.route('/')
class OrderList(Resource):
    @api.doc('Add new order', params={
            'x-access-tokens': {
                'description': 'Bearer token for authentication',
                'in': 'header',
                'type': 'string',
            }
        })
    @api.expect(_order, validate=True)
    @authentication.token_required()
    def post(_, self):
        data = request.json
        if data.get('status', None) is None:
            data['status'] = 'pending'

        # payload validations
        try:
            OrderApi.validate_status(data['status'])
        except ValueError as e:
            res_obj = {
                'status': 'failure',
                'message': str(e)
            }
            return res_obj, 400

        try:
            order_service.add_order(data)
            res_obj = {
                'status': 'success',
                'message': 'Order added successfully'
            }
            return res_obj, 201
        except RestaurantNotExistsException as e:
            res_obj = {
                'status': 'failure',
                'message': str(e)
            }
            return res_obj, 400
        except LeadNotExistsException:
            res_obj = {
                'status': 'failure',
                'message': 'Lead does not exist, send correct lead id'
            }
            return res_obj, 400
        except Exception:
            print(traceback.format_exc())
            res_obj = {
                'status': 'failure',
                'message': 'Internal server error'
            }
            return res_obj, 500

    @api.doc('get all orders', params={
            'x-access-tokens': {
                'description': 'Bearer token for authentication',
                'in': 'header',
                'type': 'string',
            }
        })
    @api.expect(parser)
    def get(self):
        args = parser.parse_args()
        if args.get('status') is not None:
            choices=['completed', 'placed', 'pending', 'cancelled', 'shipped']
            for status in args['status']:
                if status not in choices:
                    return {
                                "errors": {
                                    "status": f"The value '{status}' is not a valid choice for 'status'."
                                },
                                "message": "Input payload validation failed"
                            }, 400
        
        try:
            orders = order_service.get_orders(args)
            res_obj = {
                'status': 'success',
                'data': orders
            }
            return res_obj, 200
        except Exception:
            print(traceback.format_exc())
            res_obj = {
                'status': 'failure',
                'message': 'Internal server error'
            }
            return res_obj, 500


@api.route('/<int:order_id>')
@api.param('order_id', 'The order identifier')
class Order(Resource):
    @api.doc('get an order', params={
            'x-access-tokens': {
                'description': 'Bearer token for authentication',
                'in': 'header',
                'type': 'string',
            }
        })
    def get(self, order_id):
        order = order_service.get_order(order_id)
        if order is None:
            res_obj = {
                'status': 'failure',
                'message': 'Order not found'
            }
            return res_obj, 404
        else:
            res_obj = {
                'status': 'success',
                'data': order
            }
            return order, 200
