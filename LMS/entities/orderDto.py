from flask_restx import Namespace, fields

from datetime import datetime

class OrderApi:
    api = Namespace('order', description="Order related operations")

    @staticmethod
    def validate_status(value):
        valid_statuses = ['completed', 'placed', 'pending', 'cancelled', 'shipped']
        if value is not None and value not in valid_statuses:
            raise ValueError(f"Order status must be one of {valid_statuses}")

    order = api.model('order', {
        'status': fields.String(required=False, description="order status", default="pending"),
        'amount': fields.Float(required=True, description="order amount"),
        'lead_id': fields.Integer(required=True, description="lead id"),
        'restaurant_id': fields.Integer(required=True, description="restaurant id")
    })

class OrderDto:
    def __init__(self, status, amount, lead_id, restaurant_id, created_at):
        self.status = status
        self.amount = amount
        self.lead_id = lead_id
        self.restaurant_id = restaurant_id
        self.created_at = created_at

class OrderAdapter:
    def convert_dict_to_Dto(self, data: dict):
        return OrderDto(data['status'], data['amount'], data['lead_id'], data['restaurant_id'], data.get('created_at', datetime.now()))

    def convert_to_dict(self, data: OrderDto):
        return {
            'status': data.status,
            'amount': data.amount,
            'lead_id': data.lead_id,
            'restaurant_id': data.restaurant_id,
            'created_at': str(data.created_at)
        }

    def convert_db_object_to_Dto(self, db_object):
        return OrderDto(db_object.status, db_object.amount, db_object.lead_id, db_object.restaurant_id, db_object.created_at)


class OrderFilterDto:
    def __init__(self, order_id=None, lead_id=None, restaurant_id=None, amount=None, status=None, from_date=None, to_date=None):
        self.order_id = order_id
        self.status = status
        self.amount = amount
        self.lead_id = lead_id
        self.restaurant_id = restaurant_id
        self.from_date = from_date
        self.to_date = to_date

class OrderFilterAdapter:
    def convert_dict_to_Dto(self, data: dict):
        return OrderFilterDto(data.get('order_id', None), data.get('lead_id', None),
                               data.get('restaurant_id', None), data.get('amount', None),
                               data.get('status', None),  data.get('from_date', None),
                               data.get('to_date', None))

    def convert_to_dict(self, data: OrderFilterDto):
        return {
            'order_id': data.order_id,
            'status': data.status,
            'amount': data.amount,
            'lead_id': data.lead_id,
            'restaurant_id': data.restaurant_id,
            'from_date': data.from_date,
            'to_date': data.to_date
        }

    # def convert_db_object_to_Dto(self, db_object):
    #     return OrderFilterDto(db_object.status, db_object.amount, db_object.lead_id,
    #                            db_object.restaurant_id, db_object.created_at)


