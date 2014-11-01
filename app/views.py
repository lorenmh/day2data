from app import app, db
from models import *

@app.route('/')
def index():
    return ''

# get: return login page
# post: attempt login
@app.route('/login/')
def login():
    return ''

# get: return login template?
# post: attempt login
@app.route('/api/login/')

# get: return user details
# put / post: update user details
@app.route('/api/u/<user_id>/')
def api_user(user_id):
    return ''

# get: return all record
# post: create new record
@app.route('/api/u/<user_id>/r/')
def api_record_index(user_id):
    return ''

# get: return record
# put / post: update record
@app.route('/api/u/<user_id>/r/<record_id>/')
def api_record(user_id, record_id):
    return ''

# get: return all sets
# post: create new set
@app.route('/api/u/<user_id>/r/<record_id>/s/')
def api_set_index(user_id, record_id):
    return ''

# get: return set
# put / post: update set
@app.route('/api/u/<user_id>/r/<record_id>/s/<set_id>')
def api_set(user_id, record_id, set_id):
    return ''

# get: return all data
# post: create new data
@app.route('/api/u/<user_id>/r/<record_id>/s/<set_id>/d/')
def api_data_index(user_id, record_id, set_id):
    return ''

# get: return data
# put / post: update data
@app.route('/api/u/<user_id>/r/<record_id>/s/<set_id>/d/<data_id>/')
def api_data(user_id, record_id, set_id, data_id):
    return ''