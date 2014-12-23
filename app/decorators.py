import json
from functools import wraps
from flask import request, session
from .models import User, Record, Set
from api_response import response_success_200, response_error_400
from .redis_auth import auth_token_valid

def api_error_message(text):
    return json.dumps({'error': text})

def get_post_data(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.method == 'POST':
            values = request.get_json(force=True)
            if 'token' in values:
                token = values.pop('token')
                if auth_token_valid(values.get('token')):
                    kwargs['values'] = values
                    return fn(*args, **kwargs)
            return response_error_400({'token': 'Invalid token'})
        return fn(*args, **kwargs)
    return wrapper


def get_user_or_404(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = kwargs.pop('user_id')
        user = User.with_username(user_id)
        if user != None:
            kwargs['user'] = user
            return fn(*args, **kwargs)
        else:
            return api_error_message("user_id not found"), 404
    return wrapper

def get_record_or_404(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = kwargs["user"]
        record_id = kwargs.pop('record_id')
        record = user.get_record_with_res_id(record_id)
        if record != None:
            kwargs["record"] = record
            return fn(*args, **kwargs)
        else:
            return api_error_message("record_id not found"), 404
    return wrapper

def get_set_or_404(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        record = kwargs["record"]
        set_id = kwargs.pop('set_id')
        set = record.get_set_with_res_id(set_id)
        if set != None:
            kwargs["set"] = set
            return fn(*args, **kwargs)
        else:
            return api_error_message("set_id not found"), 404
    return wrapper

def get_data_or_404(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        set = kwargs["set"]
        data_id = kwargs.pop('data_id')
        data = set.get_data_with_res_id(data_id)
        if data != None:
            kwargs["data"] = data
            return fn(*args, **kwargs)
        else:
            return api_error_message("data_id not found"), 404
    return wrapper