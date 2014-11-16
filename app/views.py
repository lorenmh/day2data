from flask import render_template, send_from_directory, request
from app import app, db
from decorators import (get_user_or_404, get_record_or_404, get_set_or_404, 
    get_data_or_404)
import serializers, json, os
from models import User, Record, Set
from redis_login import can_attempt_login, set_failed_login
from redis_auth import auth_token_valid, touch_auth_token

#r_key = redis.StrictRedis(host='localhost', port=6379, db=1)

def api_error_message(text):
    return json.dumps({'error': text})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(os.path.join('static', path))

@app.route('/api/login', methods=['POST'])
def login():
    address = request.remote_addr
    if can_attempt_login(address):
        username = request.form["username"]
        password = request.form["password"]
        user = User.with_username(username)
        if user:
            if user.matches_password(password):
                return 'logged in!'
            else:
                set_failed_login(address)
                return api_error_message("username password combination incorrect"), 400
        else:
            return api_error_message("username password combination incorrect"), 400
    else:
        return api_error_message("maximum number of login attempts exceeded, please try again later"), 400


# get: return user details
# put / post: update user details
@app.route('/api/u/<user_id>/')
@get_user_or_404
def api_user(user):
    #user = User.with_username(user_id)
    return json.dumps(serializers.user(user))

# get: return all record
# post: create new record
@app.route('/api/u/<user_id>/r/')
@get_user_or_404
def api_record_index(user):
    return json.dumps(serializers.user_records(user))

# get: return record
# put / post: update record
@app.route('/api/u/<user_id>/r/<record_id>/')
@get_user_or_404
@get_record_or_404
def api_record(user, record):
    return json.dumps(serializers.record(record))

# get: return all sets
# post: create new set
@app.route('/api/u/<user_id>/r/<record_id>/s/')
@get_user_or_404
@get_record_or_404
def api_set_index(user, record):
    return json.dumps(serializers.record_sets(record))

# get: return set
# put / post: update set
@app.route('/api/u/<user_id>/r/<record_id>/s/<set_id>/')
@get_user_or_404
@get_record_or_404
@get_set_or_404
def api_set(user, record, set):
    return json.dumps(serializers.set(set))

# get: return all data
# post: create new data
@app.route('/api/u/<user_id>/r/<record_id>/s/<set_id>/d/')
@get_user_or_404
@get_record_or_404
@get_set_or_404
def api_data_index(user, record, set):
    return json.dumps(serializers.set_data(set))

# get: return data
# put / post: update data
@app.route('/api/u/<user_id>/r/<record_id>/s/<set_id>/d/<data_id>/')
@get_user_or_404
@get_record_or_404
@get_set_or_404
@get_data_or_404
def api_data(user, record, set, data):
    return json.dumps(serializers.data(set, data))