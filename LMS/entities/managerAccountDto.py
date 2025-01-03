from flask_restx import Namespace, fields

class ManagerAccountApi:
    api = Namespace('manager_account', description="Manager account related operations")

    @staticmethod
    def validate_role(value):
        valid_roles = ['employee', 'admin']
        if value is not None and value not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}")
    
    @staticmethod
    def validate_status(value):
        valid_statuses = ['active', 'inactive', 'suspended']
        if value is not None and value not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")

    manager_account = api.model('manager_account', {
        'username': fields.String(required=True, description="username"),
        'password': fields.String(required=True, description="password"),
        'role': fields.String(required=False, description="role", default="employee"),
        'status': fields.String(required=False, description="status", default="active")
    })

class ManagerAccountDto:
    def __init__(self, username, password, role, status):
        self.username = username
        self.password = password
        self.role = role
        self.status = status

class ManagerAccountResponseDto:
    def __init__(self, username, role, status):
        self.username = username
        self.role = role
        self.status = status

class ManagerAccountAdapter:
    def convert_dict_to_Dto(self, data: dict):
        return ManagerAccountDto(data['username'], data['password'], data['role'], data['status'])

    def convert_to_dict(self, data: ManagerAccountDto):
        return {
            'username': data.username,
            'password': data.password,
            'role': data.role,
            'status': data.status
        }

    def convert_response_dto_to_dict(self, response_dto: ManagerAccountResponseDto):
        return {
            'username': response_dto.username,
            'role': response_dto.role,
            'status': response_dto.status
        }
    
    def convert_db_obj_to_Dto(self, db_object):
        return ManagerAccountDto(db_object.username, db_object.password, db_object.role, db_object.status)

    def convert_db_object_to_response_Dto(self, db_object):
        return ManagerAccountResponseDto(db_object.username, db_object.role, db_object.status)

class ManagerAccountPerformanceResponseDto:
    def __init__(self, username, role, status, total_leads, success_leads):
        self.username = username
        self.role = role
        self.status = status
        self.total_leads = total_leads
        self.success_leads = success_leads

class ManagerAccountPerformanceResponseAdapter:
    def convert_dict_to_Dto(self, data: dict):
        return ManagerAccountPerformanceResponseDto(data['username'], data['role'], data['status'],
                                                    data['total_leads'], data['success_leads'])

    def convert_to_dict(self, data: ManagerAccountPerformanceResponseDto):
        return {
            'username': data.username,
            'role': data.role,
            'status': data.status,
            'total_leads': data.total_leads,
            'success_leads': data.success_leads
        }
    
    def convert_db_object_to_Dto(self, db_object):
        return ManagerAccountPerformanceResponseDto(db_object.username, db_object.role, db_object.status,
                                                        db_object.total_leads, db_object.successful_leads)

class ManagerAccountLoginDto:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class ManagerAccountLoginAdapter:
    def convert_dict_to_dto(self, data: dict):
        return ManagerAccountLoginDto(data['username'], data['password'])

    def convert_to_dict(self, data: ManagerAccountLoginDto):
        return {
            'username': data.username,
            'password': data.password
        }
