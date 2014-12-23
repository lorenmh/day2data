from flask import session, request, Response
from redis_auth import touch_auth_token
import json

def response_error_post(msg):
    token = touch_auth_token( request.cookies.get('XSRF-TOKEN') )
    res = Response(
        response = json.dumps({'error':True, 'message': msg}),
        status = 400,
        mimetype = "application/json",
    )
    res.set_cookie('XSRF-TOKEN', token)
    return res


def response_success_post(msg):
    token = touch_auth_token( request.cookies.get('XSRF-TOKEN') )
    res = Response(
        response = json.dumps({'success': True, 'message': msg}),
        status = 200,
        mimetype = "application/json",
    )
    res.set_cookie('XSRF-TOKEN', token)
    return res
