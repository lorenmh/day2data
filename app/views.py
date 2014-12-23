from flask import render_template, send_from_directory, request, session
from app import app, db
from decorators import (get_user_or_404, get_record_or_404, get_set_or_404, 
    get_data_or_404, get_post_data)
import serializers, json, os
from models import User, Record, Set, DATA_TYPE_CLASS
from redis_login import can_attempt_login, set_failed_login
from redis_auth import auth_token_valid, touch_auth_token
from api_response import response_success_200, response_error_400

#r_key = redis.StrictRedis(host='localhost', port=6379, db=1)

def api_error_message(text):
    return json.dumps({'error': text})

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/<path:path>')
def all(path):
    return render_template('index.html')

@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(os.path.join('static', path))

@app.route('/api/login', methods=['POST'])
def login():
    address = request.remote_addr
    if can_attempt_login(address):
        username = request.json["id"]
        password = request.json["password"]
        user = User.with_username(username)
        if user:
            if user.matches_password(password):
                session['id'] = username
                return response_success_200(serializers.user(user))
            else:
                set_failed_login(address)
                return response_error_400("username password combination incorrect")
        else:
            set_failed_login(address)
            return response_error_400("username password combination incorrect")
    else:
        return response_error_400("maximum number of login attempts exceeded, please try again later")

@app.route('/api/logout')
def logout():
    session.pop('id', None)
    return '', 200

@app.route('/api/init', methods=["GET"])
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
        return response_success_200(serializers.user(user))
    else:
        return response_error_400(validation)

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
            return response_success_200(serializers.user(user))
        else:
            return response_error_400(validation)

# get: return all record
# post: create new record
@app.route('/api/u/<user_id>/r/', methods=['GET', 'POST'])
@get_user_or_404
@get_post_data
def api_record_index(user, values=None):
    if request.method == 'GET':
        return json.dumps(serializers.user_records(user))
    else:
        validation = Record.validate(values)
        if validation == True:
            r = Record.from_values(values)
            return response_success_200(serializers.record(r))
        else:
            return response_error_400(validation)

# get: return record
# put / post: update record
@app.route('/api/u/<user_id>/r/<record_id>/', methods=['GET', 'POST'])
@get_user_or_404
@get_record_or_404
@get_post_data
def api_record(user, record, values=None):
    if request.method == 'GET':
        return json.dumps(serializers.record(record))
    else: 
        #TODO: add editing stuff
        return 'blah'


# get: return all sets
# post: create new set
@app.route('/api/u/<user_id>/r/<record_id>/s/', methods=['GET', 'POST'])
@get_user_or_404
@get_record_or_404
@get_post_data
def api_set_index(user, record, values=None):
    if request.method == 'GET':
        return json.dumps(serializers.record_sets(record))
    else:
        validation = Set.validate(values)
        if validation == True:
            data_set = Set.from_values(record=record, values=values)
            return response_success_200(serializers.set(data_set))
        else:
            return response_error_400(validation)


# get: return set
# put / post: update set
@app.route('/api/u/<user_id>/r/<record_id>/s/<set_id>/')
@get_user_or_404
@get_record_or_404
@get_set_or_404
@get_post_data
def api_set(user, record, set, values=None):
    return json.dumps(serializers.set(set))

# get: return all data
# post: create new data
@app.route('/api/u/<user_id>/r/<record_id>/s/<set_id>/d/', methods=['GET', 'POST'])
@get_user_or_404
@get_record_or_404
@get_set_or_404
@get_post_data
def api_data_index(user, record, set, values=None):
    if request.method == 'GET':
        return json.dumps(serializers.set_data(set))
    else:
        DataClass = DATA_TYPE_CLASS[set.data_type]
        validation = DataClass.validate(set=set, values=values)
        if validation == True:
            data = DataClass.from_values(set=set, values=values)
            return response_success_200(serializers.data(set, data))
        else:
            return response_error_400(validation)

# get: return data
# put / post: update data
@app.route('/api/u/<user_id>/r/<record_id>/s/<set_id>/d/<data_id>/')
@get_user_or_404
@get_record_or_404
@get_set_or_404
@get_data_or_404
@get_post_data
def api_data(user, record, set, data, values=None):
    return json.dumps(serializers.data(set, data))