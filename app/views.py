from flask import render_template, send_from_directory, request, session, Response, make_response
from app import app, db
from decorators import (get_user_or_404, get_dataset_or_404,
    get_data_or_404, get_post_data, get_post_data_and_auth)
import serializers, json, os
from models import User, Dataset, DATA_TYPE_CLASS#, Collection
from redis_login import can_attempt_login, set_failed_login
from redis_auth import auth_token_valid, touch_auth_token
from api_response import response_success, response_error

#r_key = redis.StrictRedis(host='localhost', port=6379, db=1)

def xsrf_cookie_response(template):
    res = make_response(render_template(template), 200)
    token = touch_auth_token(request.cookies.get('XSRF-TOKEN'))
    res.set_cookie('XSRF-TOKEN', token)
    return res

@app.route('/')
def root():
    return xsrf_cookie_response('index.html')

@app.route('/api/login/', methods=['POST'])
@get_post_data
def login(values):
    address = request.remote_addr
    if can_attempt_login(address):
        username = values.get('id')
        password = values.get('password')
        user = User.with_username(username)
        if user:
            if user.matches_password(password):
                session['id'] = username
                return response_success(serializers.user(user))
            else:
                set_failed_login(address)
                return response_error("username password combination incorrect")
        else:
            set_failed_login(address)
            return response_error("username password combination incorrect")
    else:
        return response_error("maximum number of login attempts exceeded, please try again later")

@app.route('/api/logout/')
def logout():
    session.pop('id', None)
    return '', 200

@app.route('/api/init/', methods=["GET"])
def init():
    if 'id' in session:
        user = User.with_username(session["id"])
        if user:
            return json.dumps(serializers.user(user))
    return '', 200

# get: return user details
# put / post: update user details
@app.route('/api/u/', methods=['POST'])
@get_post_data
def api_user_new(values=None):
    validation = User.validate(values)
    if validation == True:
        user = User.from_values(values)
        session['id'] = user.username
        return response_success(serializers.user(user))
    else:
        return response_error(validation)

# get: return user details
# put / post: update user details
@app.route('/api/u/<user_id>/', methods=['GET'])
@get_user_or_404
def api_user(user):
    if request.method == 'GET':
        return json.dumps(serializers.user(user))
    else:
        values = request.get_json(force=True)
        validation = User.validate(values)
        if validation == True:
            user = User.from_values(values)
            session['id'] = user.username
            return response_success(serializers.user(user))
        else:
            return response_error(validation)

# get: return all sets
# post: create new set
@app.route('/api/s/', methods=['GET', 'POST'])
@get_user_or_404
@get_post_data_and_auth
def api_dataset_index(user, values=None):
    if request.method == 'GET':
        return json.dumps(serializers.user_datasets(user))
    else:
        validation = Dataset.validate(values)
        if validation == True:
            dataset = Dataset.from_values(user=user, values=values)
            return response_success(serializers.dataset(dataset))
        else:
            return response_error(validation)

@app.route('/api/s/<dataset_id>/')
@get_user_or_404
@get_dataset_or_404
def api_dataset(user, dataset, values=None):
    return json.dumps(serializers.dataset(dataset))

# get: return all data
# post: create new data
@app.route('/api/s/<dataset_id>/d/', methods=['GET', 'POST'])
@get_user_or_404
@get_dataset_or_404
@get_post_data_and_auth
def api_dataset_data_index(user, dataset, values=None):
    if request.method == 'GET':
        return json.dumps(serializers.dataset_data(dataset))
    else:
        DataClass = DATA_TYPE_CLASS[dataset.data_type]
        validation = DataClass.validate(dataset=dataset, values=values)
        if validation == True:
            data = DataClass.from_values(dataset=dataset, values=values)
            return response_success(serializers.data(dataset, data))
        else:
            return response_error(validation)

@app.route('/api/u/<user_id>/s/<dataset_id>/d/<data_id>/')
@get_user_or_404
@get_dataset_or_404
@get_data_or_404
def api_dataset_data(user, dataset, data, values=None):
    return json.dumps(serializers.data(dataset, data))

# get: return all sets
# post: create new set
@app.route('/api/u/<user_id>/s/')
@get_user_or_404
def api_user_dataset_index(user):
    return json.dumps(serializers.user_datasets(user))

# get: return set
# put / post: update set
@app.route('/api/u/<user_id>/s/<dataset_id>/')
@get_user_or_404
@get_dataset_or_404
def api_user_set(user, dataset):
    return json.dumps(serializers.dataset(dataset))

# get: return all data
# post: create new data
@app.route('/api/u/<user_id>/s/<dataset_id>/d/')
@get_user_or_404
@get_dataset_or_404
def api_user_dataset_data_index(user, dataset):
    return json.dumps(serializers.dataset_data(dataset))

# get: return data
# put / post: update data
@app.route('/api/u/<user_id>/s/<dataset_id>/d/<data_id>/')
@get_user_or_404
@get_dataset_or_404
@get_data_or_404
def api_user_dataset_data(user, dataset, data):
    return json.dumps(serializers.data(dataset, data))

@app.route('/api/<path:path>')
def api_404(path):
    return response_error({'path': 'no resource at this path'})

@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(os.path.join('static', path))

#returns the app template if the route doesnt start with api or static
#@app.route('/<regex("(?!(?:api|static)).*"):path>')
@app.route('/<path:path>')
def all(path):
    return xsrf_cookie_response('index.html')