from functools import wraps
from .models import User, Record, Set

def api_error_message(text):
    return json.dumps({'error': text})

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
        data = set.get_data_with_res_id(set_id)
        if data != None:
            kwargs["data"] = data
            return fn(*args, **kwargs)
        else:
            return api_error_message("data_id not found"), 404
    return wrapper