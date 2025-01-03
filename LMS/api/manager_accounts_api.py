import traceback

from flask import request, current_app
from flask_restx import Resource

from LMS.exceptions import ManagerAccountExistsException, ManagerAccountNotExistsException, AuthenticationException
from LMS.entities import ManagerAccountApi
from LMS.service import ManagerAccountService
from LMS.utils import authentication

api = ManagerAccountApi.api
_manager_account = ManagerAccountApi.manager_account
manager_accounts_service = ManagerAccountService()


@api.route('/')
class ManagerAccountList(Resource):
    @api.doc('Add new manager account')
    @api.expect(_manager_account, validate=True)
    def post(self):
        data = request.json
        if data.get('status', None) is None:
            data['status'] = 'active'
        if data.get('role', None) is None:
            data['role'] = 'employee'

        # payload validations
        try:
            ManagerAccountApi.validate_status(data['status'])
            ManagerAccountApi.validate_role(data['role'])
        except ValueError as e:
            res_obj = {
                'status': 'failure',
                'message': str(e)
            }
            return res_obj, 400

        try:
            manager_accounts_service.add_manager_account(data)
            res_obj = {
                'status': 'success',
                'message': 'Manager account added successfully'
            }
            return res_obj, 201
        except ManagerAccountExistsException:
            res_obj = {
                'status': 'failure',
                'message': 'Manager account already exists'
            }
            return res_obj, 409
        except Exception:
            print(traceback.format_exc())
            res_obj = {
                'status': 'failure',
                'message': 'Internal server error'
            }
            return res_obj, 500

@api.route('/login')
class ManagerAccountLogin(Resource):
    login_header_parser = api.parser()
    login_header_parser.add_argument('username', location='headers')
    login_header_parser.add_argument('password', location='headers')

    @api.doc('Login with manager account')
    @api.expect(login_header_parser, validate=True)
    def post(self):
        headers = request.headers
        if not headers or not headers.get('username', None) or not headers.get('password', None):
            return {
                'status': 'failure',
                'message': 'Authentication failure'
            }, 401
        user_data = {
            'username': headers['username'],
            'password': headers['password']
        }

        try:
            token = manager_accounts_service.get_token(user_data, current_app.config['SECRET_KEY'])
            res_obj = {
                'status': 'success',
                'data': {
                    'token': token
                }
            }
            return res_obj, 200
        except ManagerAccountNotExistsException as e:
            return {
                'status': 'failure',
                'message': 'Account not exists'
            }, 404
        except AuthenticationException as e:
            return {
                'status': 'failure',
                'message': 'Authentication failure'
            }, 401
        except Exception:
            print(traceback.format_exc())
            return {
                'status': 'failure',
                'message': 'Internal server error'
            }, 500

@api.route('/<manager_account_username>')
@api.param('manager_account_username', 'Manager account identifier')
class ManagerAccount(Resource):
    @api.doc('get a manager account')
    def get(self, manager_account_username):
        manager_account = manager_accounts_service.get_manager_account(manager_account_username)
        if manager_account is None:
            res_obj = {
                'status': 'failure',
                'message': 'Manager account not found'
            }
            return res_obj, 404
        else:
            res_obj = {
                'status': 'success',
                'data': manager_account
            }
            return res_obj, 200

@api.route('/account_performance')
class ManagerAccountPerformance(Resource):
    token_parser = api.parser()
    token_parser.add_argument('x-access-tokens', location='headers')

    @api.doc('get account performance')
    @authentication.admin_token_required()
    @api.expect(token_parser, validate=True)
    def get(_, self):
        try:
            account_performance = manager_accounts_service.get_all_manager_account_performance()
            res_obj = {
                'status': 'success',
                'data': account_performance
            }
            return res_obj, 200
        except Exception:
            print(traceback.format_exc())
            res_obj = {
                'status': 'failure',
                'message': 'Internal server error'
            }
            return res_obj, 500
