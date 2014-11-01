import json
from datetime import datetime
from app.models import User, Choice, DATA_TYPE_INT, DATA_TYPE_STR

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

def count_data_short(data):
    srl = {
        "id": data.res_id,
        "timestamp": dt_to_ms(data.timestamp)
    }
    return srl

def value_data_short(data):
    srl = {
        "id": data.res_id,
        "timestamp": dt_to_ms(data.timestamp),
        "value": data.value
    }
    return srl

def timed_data_short(data):
    srl = {
        "id": data.res_id,
        "start": dt_to_ms(data.start),
        "stop": dt_to_ms(data.stop)
    }
    return srl

def choice_data_short(data):
    srl = {
        "id": data.res_id,
        "choice": data.choice
    }
    return srl

def choice_set_key(set):
    choices = Choice.for_set(set.id)
    key = {}
    for choice in choices:
        key[choice.res_id] = choice.title
    return key

def data_short_for_type(set):
    if set.type == DATA_TYPE_INT["count"]:
        return [count_data_short(d) for d in set.get_data_all()]
    elif set.type == DATA_TYPE_INT["value"]:
        return [value_data_short(d) for d in set.get_data_all()]
    elif set.type == DATA_TYPE_INT["timed"]:
        return [timed_data_short(d) for d in set.get_data_all()]
    elif set.type == DATA_TYPE_INT["choice"]:
        return [choice_data_short(d) for d in set.get_data_all()]
    else:
        return None

def set(set):
    srl = set_short(set)
    srl["set"]["unit"] = set.unit
    srl["set"]["unit_short"] = set.unit_short
    srl["set"]["data"] = data_short_for_type(set)
    return srl


def set_short(set):
    srl = {
        "set": {
            "id": set.res_id,
            "title": set.title,
            "text": set.text,
            "timestamp": dt_to_ms(set.timestamp),
            "type": DATA_TYPE_STR[set.type]
        }
    }

    if set.type == DATA_TYPE_INT["choice"]:
        srl["set"]["key"] = choice_set_key(set)

    return srl


def record(rcd):
    srl = record_short(rcd)
    srl["record"]["sets"] = [set_short(set) for set in rcd.get_set_all()]
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
    return srl