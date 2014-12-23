from flask import render_template, send_from_directory, request, session
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
                return json.dumps(serializers.user(user))
            else:
                set_failed_login(address)
                return api_error_message("username password combination incorrect"), 400
        else:
            set_failed_login(address)
            return api_error_message("username password combination incorrect"), 400
    else:
        return api_error_message("maximum number of login attempts exceeded, please try again later"), 400

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
@app.route('/api/u/<user_id>/')
@get_user_or_404
def api_user(user):
    #user = User.with_username(user_id)
    return json.dumps(serializers.user(user))

# get: return all record
# post: create new record
@app.route('/api/u/<user_id>/r/', methods=['GET', 'POST'])
@get_user_or_404
def api_record_index(user):
    if request.method == 'GET':
        return json.dumps(serializers.user_records(user))
    else:
        values = request.get_json(force=True)
        validation = Record.validate(values)
        if validation == True:
            title, text, permissions_view = values.get('title'), values.get('text'), values.get('permissions_view')
            rcrd = Record(title=title, owner=user.id, text=text, permissions_view=permissions_view)
            rcrd.create()
            return json.dumps({ 'success': True, 'record': serializers.record(rcrd) })
        else:
            return json.dumps({ 'errors': validation })

# get: return record
# put / post: update record
@app.route('/api/u/<user_id>/r/<record_id>/', methods=['GET', 'POST'])
@get_user_or_404
@get_record_or_404
def api_record(user, record):
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
def api_set_index(user, record):
    if request.method == 'GET':
        return json.dumps(serializers.record_sets(record))
    else:
        values = request.get_json(force=True)
        validation = Set.validate(values)
        if validation == True:
            title, text, type, unit, unit_short = values.get('title'), values.get('text'), int(values.get('type')), values.get('unit'), values.get('unit_short')
            set = Set(title=title, record=record.id, type=type, text=text, unit=unit, unit_short=unit_short)
            set.create()
            return json.dumps({ 'success': True, 'set': serializers.set(set) })
        else:
            return json.dumps({ 'errors': validation })


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