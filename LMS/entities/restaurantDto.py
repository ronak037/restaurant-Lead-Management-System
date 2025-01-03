from flask_restx import Namespace, fields

class RestaurantApi:
    api = Namespace('restaurant', description="Restaurant related operations")
    restaurant = api.model('restaurant', {
        'name': fields.String(required=True, description="restaurant name"),
        'location': fields.String(required=True, description="restaurant location"),
    })

class RestaurantDto:
    def __init__(self, name, location):
        self.name = name
        self.location = location

class RestaurantAdapter:
    def convert_dict_to_Dto(self, data: dict):
        return RestaurantDto(data['name'], data['location'])
    
    def convert_to_dict(self, data: RestaurantDto):
        return {
            'name': data.name,
            'location': data.location
        }

    def convert_db_object_to_Dto(self, db_object):
        return RestaurantDto(db_object.name, db_object.location)
