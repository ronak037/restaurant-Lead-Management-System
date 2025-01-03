from LMS.db import db
from LMS.models import Orders
from LMS.entities import OrderAdapter

class OrderRepository:
    def __init__(self):
        self.order_adapter = OrderAdapter()

    def __filter_orders(self, query, filters):
        # Extracting each filter from the 'filters' dictionary (which is passed from reqparse)
        if filters.get('order_id'):
            query = query.filter(Orders.id.in_(filters['order_id']))
        if filters.get('lead_id'):
            query = query.filter(Orders.lead_id.in_(filters['lead_id']))
        if filters.get('restaurant_id'):
            query = query.filter(Orders.restaurant_id.in_(filters['restaurant_id']))
        if filters.get('amount'):
            query = query.filter(Orders.amount.in_(filters['amount']))
        if filters.get('status'):
            query = query.filter(Orders.status.in_(filters['status']))
        if filters.get('from_date'):
            query = query.filter(Orders.created_at >= filters['from_date'])
        if filters.get('to_date'):
            query = query.filter(Orders.created_at <= filters['to_date'])
        return query.all()

    def add_order(self, order_dto):
        order = Orders(
            status = order_dto.status,
            amount = order_dto.amount,
            lead_id = order_dto.lead_id,
            restaurant_id = order_dto.restaurant_id,
            created_at = order_dto.created_at
        )
        self.save_db(order)
    
    def get_order(self, order_id):
        db_order = Orders.query.filter_by(id=order_id).first()
        if db_order is None:
            return None
        # convert to dto
        order_dto = self.order_adapter.convert_db_object_to_Dto(db_order)
        return order_dto
    
    def get_filtered_orders(self, order_filter_dto):
        attrs = vars(order_filter_dto)
        filter_condition = {k: v for k, v in attrs.items() if v is not None}
        query = Orders.query
        res = self.__filter_orders(query, filter_condition)

        order_dto_list = []
        for db_order in res:
            order_dto = self.order_adapter.convert_db_object_to_Dto(db_order)
            order_dto_list.append(order_dto)
        return order_dto_list

    def save_db(self, data):
        db.session.add(data)
        db.session.commit()
