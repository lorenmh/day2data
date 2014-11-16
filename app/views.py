from app import app, db
from decorators import (get_user_or_404, get_record_or_404, get_set_or_404, 
    get_data_or_404)
import serializers, json, os
from models import User, Record, Set
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/js/<path:path>')
def static_js(path):
    return app.send_static_file(os.path.join('js', path))

'''
# get: return login page
# post: attempt login
@app.route('/login/')
def login():
    return ''

# get: return login template?
# post: attempt login
@app.route('/api/login/')
def api_login():
    return '''

# get: return user details
# put / post: update user details
@app.route('/api/u/<user_id>/')
@get_user_or_404
def api_user(user):
    #user = User.with_username(user_id)
    return serializers.user(user)

# get: return all record
# post: create new record
@app.route('/api/u/<user_id>/r/')
@get_user_or_404
def api_record_index(user):
    return serializers.user_records(user)

# get: return record
# put / post: update record
@app.route('/api/u/<user_id>/r/<record_id>/')
@get_user_or_404
@get_record_or_404
def api_record(user, record):
    return serializers.record(record)

# get: return all sets
# post: create new set
@app.route('/api/u/<user_id>/r/<record_id>/s/')
@get_user_or_404
@get_record_or_404
def api_set_index(user, record):
    return serializers.record_sets(record)

# get: return set
# put / post: update set
@app.route('/api/u/<user_id>/r/<record_id>/s/<set_id>/')
@get_user_or_404
@get_record_or_404
@get_set_or_404
def api_set(user, record, set):
    return serializers.set(set)

# get: return all data
# post: create new data
@app.route('/api/u/<user_id>/r/<record_id>/s/<set_id>/d/')
@get_user_or_404
@get_record_or_404
@get_set_or_404
def api_data_index(user, record, set):
    return serializers.set_data(set)

# get: return data
# put / post: update data
@app.route('/api/u/<user_id>/r/<record_id>/s/<set_id>/d/<data_id>/')
@get_user_or_404
@get_record_or_404
@get_set_or_404
@get_data_or_404
def api_data(user, record, set, data):
    return serializers.data(set, data)