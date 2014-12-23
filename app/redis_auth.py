import redis, time, json, hashlib, binascii, os

# fuck you python
secret = 'super duper fucking secret'

from datetime import datetime

r_auth = redis.StrictRedis(host='localhost', port=6379, db=1)

def dt_to_seconds(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def dt_to_ut(dt):
    return int(dt_to_seconds(dt) * 1000)

def create_token(length):
    return binascii.b2a_hex(os.urandom(int(length / 2)))

def touch_auth_token(token=None):
    if token != None:
        r_auth.delete(token)
    now_ut = dt_to_ut(datetime.utcnow())
    token = create_token(32)
    r_auth.set(token, json.dumps(now_ut))
    return token

def auth_token_valid(token):
    if token != None:
        auth = r_auth.get(token)
        if auth != None:
            return True
    return False