from LMS.service import ManagerAccountService

from functools import wraps
from flask import request, current_app

import jwt

def token_required(raise_exception=True):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = None
            if 'x-access-tokens' in request.headers:
                token = request.headers['x-access-tokens']
            if not token:
                if raise_exception:
                    return {
                        'status': 'failure',
                        'message': 'Not a valid token'
                    }, 401
                return f(None, *args, **kwargs)

            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                current_user = ManagerAccountService().get_manager_account(account_username=data['username'])
                if current_user is None:
                    raise Exception
            except Exception:
                if raise_exception:
                    return {
                        'status': 'failure',
                        'message': 'Not a valid token'
                    }, 401
                return f(None, *args, **kwargs)
            
            return f(current_user, *args, **kwargs)
        return wrapper
    return decorator

def admin_token_required(raise_exception=True):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = None
            if 'x-access-tokens' in request.headers:
                token = request.headers['x-access-tokens']
            
            if not token:
                if raise_exception:
                    return {
                        'status': 'failure',
                        'message': 'Not a valid admin token'
                    }, 401
                return f(None, *args, **kwargs)
            
            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                current_user = ManagerAccountService().get_manager_account(account_username=data['username'])
                if current_user is None or current_user['role']!='admin':
                    raise Exception
            except Exception:
                if raise_exception:
                    return {
                        'status': 'failure',
                        'message': 'Not a valid admin token'
                    }, 401
                return f(None, *args, **kwargs)
            
            return f(current_user, *args, **kwargs)
        return wrapper
    return decorator
