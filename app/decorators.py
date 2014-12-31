import json
from functools import wraps
from flask import request, session
from .models import User, Dataset#, Collection
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

def get_post_data_and_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.method == 'POST':
            user = kwargs["user"]
            username = session.get('id')
            if username == None or username != user.username:
                return response_error({ 'auth': 'Unauthorized request' })
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
        if 'user_id' in kwargs:
            user_id = kwargs.pop('user_id')
        else:
            user_id = session.get('id')
        user = User.with_username(user_id)
        if user != None:
            kwargs['user'] = user
            return fn(*args, **kwargs)
        else:
            return response_error( {"user_id": "user id not found"} )
    return wrapper

def get_dataset_or_404(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = kwargs["user"]
        dataset_id = kwargs.pop('dataset_id')
        dataset = user.get_dataset_with_res_id(dataset_id)
        if dataset != None:
            kwargs["dataset"] = dataset
            return fn(*args, **kwargs)
        else:
            return response_error( {"dataset_id": "dataset id not found"} )
    return wrapper

def get_data_or_404(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        dataset = kwargs["dataset"]
        data_id = kwargs.pop('data_id')
        data = dataset.get_data_with_res_id(data_id)
        if data != None:
            kwargs["data"] = data
            return fn(*args, **kwargs)
        else:
            return response_error( {"data_id": "data id not found"} )
    return wrapper