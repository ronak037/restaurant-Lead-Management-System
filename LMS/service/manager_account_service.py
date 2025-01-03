from LMS.repository import ManagerAccountRepository
from LMS.utils import Singleton
from LMS.entities import ManagerAccountAdapter, ManagerAccountResponseDto, \
                        ManagerAccountPerformanceResponseAdapter, ManagerAccountLoginAdapter
from LMS.exceptions import ManagerAccountNotExistsException, AuthenticationException

from werkzeug.security import check_password_hash
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta

import jwt

class ManagerAccountService(metaclass=Singleton):
    def __init__(self):
        self.manager_account_repo = ManagerAccountRepository()
        self.manager_account_adapter = ManagerAccountAdapter()
        self.manager_account_login_adapter = ManagerAccountLoginAdapter()
        self.manager_account_performance_adapter = ManagerAccountPerformanceResponseAdapter()

    def add_manager_account(self, manager_account_dict: dict):
        manager_account_dto = self.manager_account_adapter.convert_dict_to_Dto(manager_account_dict)
        manager_account_dto.password = pbkdf2_sha256.hash(manager_account_dto.password)
        self.manager_account_repo.add_manager_account(manager_account_dto)

    def get_manager_account(self, account_username) -> ManagerAccountResponseDto:
        manager_account_response_dto = self.manager_account_repo.get_manager_account(account_username)
        return self.manager_account_adapter.convert_response_dto_to_dict(manager_account_response_dto) if manager_account_response_dto else None
    
    def get_all_manager_account_performance(self):
        account_performances = self.manager_account_repo.get_all_account_performance()
        for i in range(0, len(account_performances)):
            account_performances[i] = self.manager_account_performance_adapter.convert_to_dict(account_performances[i])
        return account_performances
            
    def get_token(self, user_data, secret_key):
        manager_account_login_dto = self.manager_account_login_adapter.convert_dict_to_dto(user_data)
        user_info_dto = self.manager_account_repo.get_full_manager_account(manager_account_login_dto.username)
        if user_info_dto is None:
            raise ManagerAccountNotExistsException("Account doesn't exists")

        if pbkdf2_sha256.verify(manager_account_login_dto.password, user_info_dto.password):
            token = jwt.encode({
                                'username': user_info_dto.username, 
                                'exp': datetime.now()+timedelta(minutes=45)
                            }, secret_key, "HS256")
            return token
        raise AuthenticationException("Authentication failure")
