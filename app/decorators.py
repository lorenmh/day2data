import json
from functools import wraps
from flask import request, session
from .models import User, Record, DataSet
from api_response import response_success, response_error
from .redis_auth import auth_token_valid

def get_post_data(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.method == 'POST':
            token = request.headers.get('X-XSRF-TOKEN')
            if token != None:
                if auth_token_valid(token):
                    kwargs['values'] = request.get_json(force=True)
                    return fn(*args, **kwargs)
            return response_error({ 'token': 'Invalid token' })
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
            return response_error( {"user_id": "user id not found"} )
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
            return response_error( {"record_id": "record id not found"} )
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
            return response_error( {"set_id": "set id not found"} )
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
            return response_error( {"data_id": "data id not found"} )
    return wrapper