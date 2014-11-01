import json
from datetime import datetime
from app.models import User

def dt_to_seconds(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def dt_to_ms(dt):
    return int(dt_to_seconds(dt) * 1000)

def user(usr):
    srl = {
        "user": {
            "id": usr.username,
            "timestamp": dt_to_ms(usr.timestamp),
            "about": usr.about,
        }
    }
    return srl

def user_short(usr):
    srl = {
        "user": {
            "id": usr.username
        }
    }
    return srl


def c_data_short(data):
    srl = {
        "id": data.id,
        "timestamp": dt_to_ms(data.timestamp)
    }
    return srl

def v_data_short(data):
    srl = {
        "id": data.id,
        "timestamp": dt_to_ms(data.timestamp),
        "value": data.value
    }
    return srl

def t_data_short(data):
    srl = {
        "id": data.id,
        "start": dt_to_ms(data.start),
        "stop": dt_to_ms(data.stop)
    }
    return srl

def set(set):
    srl = set_short(set)["set"]
    srl["unit"] = set.unit
    srl["unit_short"] = set.unit_short
    if set.__tablename__ == "countset":
        data = [c_data_short(d) for d in set.get_data_all()]
    elif set.__tablename__ == "valueset":
        data = [v_data_short(d) for d in set.get_data_all()]
    elif set.__tablename__ == "timedset":
        data = [t_data_short(d) for d in set.get_data_all()]
    else:
        data = None
    srl["data"] = data
    return srl


def set_short(set):
    srl = {
        "set": {
            "id": set.res_id,
            "title": set.title,
            "text": set.text,
            "timestamp": dt_to_ms(set.timestamp),
            "type": set.__tablename__
        }
    }
    return srl


def record(rcd):
    srl = record_short(rcd)["record"]
    srl["sets"] = [set_short(set) for set in rcd.get_set_all()]
    return srl

def record_short(rcd):
    srl = {
        "record": {
            "id": rcd.res_id,
            "owner": user_short(User.query.get(rcd.owner)),
            "title": rcd.title,
            "text": rcd.text,
            "timestamp": dt_to_ms(rcd.timestamp)
        }
    }