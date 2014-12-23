from flask import session
from redis_auth import touch_auth_token
import json

def response_error_400(msg):
    return json.dumps({'error':True, 'message': msg}), 400

def response_success_200(msg):
    token = touch_auth_token(session.get('token'))
    session['token'] = token
    return json.dumps({'success': True, 'token': token, 'message': msg}), 200