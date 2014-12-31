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
        "id": usr.username,
        "time": dt_to_ms(usr.timestamp),
        "about": usr.about,
    }
    return srl

def user_short(usr):
    return { "id": usr.username }

def user_datasets(usr):
    return [dataset_short(s) for s in usr.get_dataset_all()]

def dataset(dataset):
    srl = dataset_short(dataset)
    srl["unit"] = dataset.unit
    srl["unit_short"] = dataset.unit_short
    srl["dataset"] = data_short_for_data_type(dataset)
    return srl


def dataset_short(dataset):
    srl = {
        "id": dataset.res_id,
        "user": user_short(User.query.get(dataset.user)),
        "title": dataset.title,
        "text": dataset.text,
        "time": dt_to_ms(dataset.timestamp),
        "data_type": DATA_TYPE_STR[dataset.data_type],
        "count": dataset.get_data_count()
    }

    return srl

def dataset_data(dataset):
    return data_short_for_data_type(dataset)

def data(dataset, data):
    if dataset.data_type == DATA_TYPE_INT["count"]:
        type = "count"
        data_info = count_data_short(data)
    elif dataset.data_type == DATA_TYPE_INT["value"]:
        type = "value"
        data_info = value_data_short(data)
    elif dataset.data_type == DATA_TYPE_INT["timed"]:
        type = "timed"
        data_info = timed_data_short(data)
    elif dataset.data_type == DATA_TYPE_INT["choice"]:
        type = "choice"
        data_info = choice_data_short(data)
    else:
        type = None
        data_info = None
    srl = {
        "data": data_info,
        "data_type": type,
        "text": data.text
    }
    return srl

def count_data_short(data):
    srl = {
        "id": data.res_id,
        "time": dt_to_ms(data.timestamp)
    }
    return srl

def value_data_short(data):
    srl = {
        "id": data.res_id,
        "time": dt_to_ms(data.timestamp),
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
        "time": dt_to_ms(data.timestamp),
        "choice": data.choice
    }
    return srl

def choice_dataset_key(dataset):
    choices = Choice.for_dataset(dataset.id)
    key = {}
    for choice in choices:
        key[choice.res_id] = choice.title
    return key

def data_short_for_data_type(dataset):
    key = None
    if dataset.data_type == DATA_TYPE_INT["count"]:
        data_type = "count"
        data_list = [count_data_short(d) for d in dataset.get_data_all()]
    elif dataset.data_type == DATA_TYPE_INT["value"]:
        data_type = "value"
        data_list = [value_data_short(d) for d in dataset.get_data_all()]
    elif dataset.data_type == DATA_TYPE_INT["timed"]:
        data_type = "timed"
        data_list = [timed_data_short(d) for d in dataset.get_data_all()]
    elif dataset.data_type == DATA_TYPE_INT["choice"]:
        data_type = "choice"
        key = choice_dataset_key(dataset)
        data_list = [choice_data_short(d) for d in dataset.get_data_all()]
    else:
        data_type = None
        data_list = None
    srl = {
        "data": data_list,
        "data_type": data_type
    }
    if key != None:
        srl["key"] = key
    return srl