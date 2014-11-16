import redis, time, json
from datetime import datetime

r_login = redis.StrictRedis(host='localhost', port=6379, db=0)

TOKEN_TIMEOUT = 's' #seconds
MAX_DAILY_ATTEMPTS = 20
MAX_RECENT_ATTEMPTS = 8

def dt_to_key(dt):
    return "%s:%s:%s" % (dt.month, dt.day, dt.year)

def dt_to_sec(dt):
    return time.mktime(dt.timetuple())

def touch_auth_token():
  pass

def auth_token_valid():
  pass