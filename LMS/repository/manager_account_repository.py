from LMS.db import db
from LMS.models import ManagerAccounts, Leads
from LMS.entities import ManagerAccountAdapter, ManagerAccountPerformanceResponseAdapter
from LMS.exceptions import ManagerAccountExistsException

from sqlalchemy.orm import defer

class ManagerAccountRepository:
    def __init__(self):
        self.manager_account_adapter = ManagerAccountAdapter()
        self.manager_account_performance_adapter = ManagerAccountPerformanceResponseAdapter()
    
    def add_manager_account(self, manager_account_dto):
        db_manager_account = ManagerAccounts.query.filter(ManagerAccounts.username==manager_account_dto.username).first()
        
        if not db_manager_account:
            manager_account = ManagerAccounts(
                username = manager_account_dto.username,
                password = manager_account_dto.password,
                role = manager_account_dto.role,
                status = manager_account_dto.status
            )
            self.save_db(manager_account)
        else:
            raise ManagerAccountExistsException

    def get_manager_account(self, username):
        db_manager_account = ManagerAccounts.query.options(defer(ManagerAccounts.password)).filter_by(username=username).first()
        if db_manager_account is None:
            return None
        # convert to dto
        manager_account_dto = self.manager_account_adapter.convert_db_object_to_response_Dto(db_manager_account)
        return manager_account_dto
    
    def get_full_manager_account(self, username):
        db_manager_account = ManagerAccounts.query.options(defer(ManagerAccounts.password)).filter_by(username=username).first()
        if db_manager_account is None:
            return None
        # convert to dto
        manager_account_dto = self.manager_account_adapter.convert_db_obj_to_Dto(db_manager_account)
        return manager_account_dto
    
    def get_all_account_performance(self):
        q_result = db.session.query(
            ManagerAccounts.username,
            ManagerAccounts.status,
            ManagerAccounts.role,
            db.func.count(Leads.id).label('total_leads'),
            db.func.sum(
                db.case(
                    (Leads.status == 'converted', 1),  # Check for 'converted' status
                    else_=0
                )
            ).label('successful_leads')
        ).join(Leads, Leads.account_username == ManagerAccounts.username) \
        .group_by(ManagerAccounts.username, ManagerAccounts.status, ManagerAccounts.role) \
        .all()

        result = []
        for r in q_result:
            result.append(self.manager_account_performance_adapter.convert_db_object_to_Dto(r))
        return result
    
    def commit_db(self):
        db.session.commit()

    def save_db(self, data):
        db.session.add(data)
        self.commit_db()
