import redis, time, json
from datetime import datetime

r_login = redis.StrictRedis(host='localhost', port=6379, db=0)

ATTEMPT_COOLDOWN = 300 #seconds
MAX_DAILY_ATTEMPTS = 20
MAX_RECENT_ATTEMPTS = 8

def dt_to_key(dt):
    return "%s:%s:%s" % (dt.month, dt.day, dt.year)

def dt_to_sec(dt):
    return int(time.mktime(dt.timetuple()))

'''
    an attempt has the following schema in redis:
    redis: {
        address: {
            recent_attempts: [ entry for each attempt in unix time in seconds (/1000)],
            daily: {
                date: "a string representing a date",
                count: an int representing the number of attempts for above date
            }
        }
    }

    ex:
    {
        "127.0.0.1": {
            recent_attempts: [1416125471, 1416125481, 1416125486],
            daily: {
                date: "11:15:2014",
                count: 12
            }
        }
    }

'''
def can_attempt_login(address):
    now = datetime.now()
    attempts = r_login.get(address)
    if attempts != None:
        attempts = json.loads(attempts)
        if attempts["daily"]["date"] == dt_to_key(now):
            if not attempts["daily"]["count"] < MAX_DAILY_ATTEMPTS:
                return False
        cleaned_attempts = []
        for attempt_dt in attempts["recent_attempts"]:
            if dt_to_sec(now) - attempt_dt <= ATTEMPT_COOLDOWN:
                cleaned_attempts.append(attempt_dt)
        attempts["recent_attempts"] = cleaned_attempts
        r_login.set(address, json.dumps(attempts))
        if not len(cleaned_attempts) < MAX_RECENT_ATTEMPTS:
            return False
    return True

def set_failed_login(address):
    now = datetime.now()
    attempts = r_login.get(address)
    if attempts == None:
        attempts = {
            "recent_attempts": [dt_to_sec(now)],
            "daily": {
                "date": dt_to_key(now),
                "count": 1
            }
        }
    else:
        attempts = json.loads(attempts)
        attempts["recent_attempts"].append(dt_to_sec(now))
        dt_key = dt_to_key(now)
        if attempts["daily"]["date"] == dt_key:
            attempts["daily"]["count"] += 1
        else:
            attempts["daily"]["date"] = dt_key
            attempts["daily"]["count"] = 1
    r_login.set(address, json.dumps(attempts))