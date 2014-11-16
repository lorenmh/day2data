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

def user_records(usr):
    srl = {
        "records": [record_short(r) for r in usr.get_record_all()]
    }
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
            "timestamp": dt_to_ms(rcd.timestamp),
            "set_count": rcd.get_set_count()
        }
    }
    return srl

def record_sets(rcd):
    srl = {
        "sets": [set_short(s) for s in rcd.get_set_all()]
    }
    return srl


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
            "type": DATA_TYPE_STR[set.type],
            "data_count": set.get_data_count()
        }
    }

    return srl

def set_data(set):
    srl = {
        "data": data_short_for_type(set)
    }
    return srl

def data(set, data):
    if set.type == DATA_TYPE_INT["count"]:
        type = "count"
        data_info = count_data_short(data)
    elif set.type == DATA_TYPE_INT["value"]:
        type = "value"
        data_info = value_data_short(data)
    elif set.type == DATA_TYPE_INT["timed"]:
        type = "timed"
        data_info = timed_data_short(data)
    elif set.type == DATA_TYPE_INT["choice"]:
        type = "choice"
        data_info = choice_data_short(data)
    else:
        type = None
        data_info = None
    srl = {
        "data": data_info,
        "type": type,
        "text": data.text
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
        "timestamp": dt_to_ms(data.timestamp),
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
    key = None
    if set.type == DATA_TYPE_INT["count"]:
        type = "count"
        data_list = [count_data_short(d) for d in set.get_data_all()]
    elif set.type == DATA_TYPE_INT["value"]:
        type = "value"
        data_list = [value_data_short(d) for d in set.get_data_all()]
    elif set.type == DATA_TYPE_INT["timed"]:
        type = "timed"
        data_list = [timed_data_short(d) for d in set.get_data_all()]
    elif set.type == DATA_TYPE_INT["choice"]:
        type = "choice"
        key = choice_set_key(set)
        data_list = [choice_data_short(d) for d in set.get_data_all()]
    else:
        type = None
        data_list = None
    srl = {
        "data": data_list,
        "type": type
    }
    if key != None:
        srl["key"] = key
    return srl