from flask_restx import Namespace, fields

class RestaurantContactApi:
    api = Namespace('restaurant_contact', description="Restaurant contact related operations")

    @staticmethod
    def validate_phone_number(value):
        if value.isdigit() == False:
            raise ValueError("Phone number must contain only digits")
        if len(value) != 10:
            raise ValueError("Phone number must be a 10 digit number")

    @staticmethod
    def validate_role(value):
        valid_roles = ['manager', 'supervisor', 'contractor']
        if value not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}")

    restaurant_contact = api.model('restaurant_contact', {
        'name': fields.String(required=True, description="restaurant contact name"),
        'role': fields.String(required=True, description="restaurant contact role"),
        'phone_number': fields.String(required=True, description="restaurant contact phone number"),
        'restaurant_id': fields.Integer(required=True, description="restaurant id")
    })

class RestaurantContactDto:
    def __init__(self, name, role, phone_number, restaurant_id):
        self.name = name
        self.role = role
        self.phone_number = phone_number
        self.restaurant_id = restaurant_id

class RestaurantContactAdapter:
    def convert_dict_to_Dto(self, data: dict):
        return RestaurantContactDto(data['name'], data['role'], data['phone_number'], data['restaurant_id'])
    
    def convert_to_dict(self, data: RestaurantContactDto):
        return {
            'name': data.name,
            'role': data.role,
            'phone_number': data.phone_number,
            'restaurant_id': data.restaurant_id
        }
    
    def convert_db_object_to_Dto(self, db_object):
        return RestaurantContactDto(db_object.name, db_object.role, db_object.phone_number, db_object.restaurant_id)
