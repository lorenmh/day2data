# coding: utf-8
from app import db, secret
from datetime import datetime
import os, binascii, bcrypt, re

VALID_PSWD_RE = "^[\w\!\@\#\$\%\^\&\*\-]{4,32}$"
VALID_EMAIL_RE = "^.+@.+\..+$"
VALID_USERNAME_RE = "^(?!.*(?:^|[_-])(?:[_-]|$))[a-z-]{3,16}$"
VALID_UNIT_SHORT_RE = "^[\w\!\(\)\-\+\[\]\,\/\#\$\%\&\*\€\£\.]{,12}$"
# 1 - 32 chars, valid a-b-c, not -a-b or a-b- or a--b. a b c matches, not a  b
# matches if false
VALID_TITLE_RE = "^(?!.*(?:^|[_-])(?:[_-]|$))[\w-]{1,32}$"

DATA_TYPE_INT = {
    "count": 1,
    "value": 2,
    "timed": 3,
    "choice": 4
}

DATA_TYPE_STR = {
    1: "count",
    2: "value",
    3: "timed",
    4: "choice"
}

PERMISSIONS_VIEW_INT = {
    "private": 1,
    "public": 2
}

PERMISSIONS_VIEW_STR = {
    1: "private",
    2: "friends",
    3: "public"
}

def dt_to_seconds(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def dt_to_ut(dt):
    return int(dt_to_seconds(dt) * 1000)

def ut_to_dt(ut):
    return datetime.fromtimestamp(ut / 1000)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(128), nullable=True, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    about = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(64))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.save()

    def get_dataset_with_res_id(self, res_id):
        return Dataset.query.filter_by(user=self.id).filter_by(res_id=res_id).first()

    def get_dataset_all(self):
        return Dataset.query.filter_by(user=self.id).all()

    @staticmethod
    def from_values(values):
        u = User(username=values.get('username'), password=values.get('password'))
        u.create()
        return u

    @staticmethod
    def validate(values=None):
        errors = {}
        if isinstance(values, dict):
            username, email, password = values.get('username'), values.get('email'), values.get('password')
            print email == ''
            if username == None:
                errors['username'] = 'Username is required'
            if password == None:
                errors['password'] = 'Password is required'
            if username != None and password != None:
                if not re.search(VALID_USERNAME_RE, username):
                    errors['username'] = 'Invalid username'
                elif User.with_username(username) != None:
                    errors['username'] = 'Username is already in use'
                if re.search(VALID_PSWD_RE, password) == None:
                    errors['password'] = 'Invalid password'
            if email != None and email != '':
                if not re.search(VALID_EMAIL_RE, email):
                    errors['email'] = 'Invalid email'
                elif email != '' and User.with_email(email) != None:
                    errors['email'] = 'Email is already in use'
        else:
            errors['username'] = 'Username is required'
            errors['password'] = 'Password is required'
        if errors == {}:
            return True
        else:
            return errors


    def __init__(self, username, password, email=None, timestamp=None, about=None):
        self.username = username
        if email != '':
            email = None
        self.email = email
        self.password = self.hash_password(password)
        self.timestamp = timestamp
        self.about = about

    def __repr__(self):
        return "<User id:%s>" % self.id

    @staticmethod
    def with_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def with_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def valid_password(pswd):
        return re.search(VALID_PSWD_RE, pswd) != None

    @staticmethod
    def valid_username(username):
        return re.search(VALID_USERNAME_RE, username) != None

    def hash_password(self, pswd):
        return bcrypt.hashpw(pswd.encode('utf-8'), bcrypt.gensalt(10))

    def matches_password(self, str):
        return bcrypt.hashpw(str.encode('utf-8'), self.password.encode('utf-8')) == self.password

# finds the current max res_id for this dataset
def next_res_id_for_data(mdl, dataset):
    last = db.session.query(mdl).filter_by(dataset=dataset).order_by("-id").first()
    if last:
        return last.res_id + 1
    return 1

class CountData(db.Model):
    __tablename__ = "countdata"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    dataset = db.Column(db.Integer, db.ForeignKey('dataset.id'))

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    text = db.Column(db.Text, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.res_id = next_res_id_for_data(CountData, self.dataset)
        self.save()

    @staticmethod
    def from_values(dataset, values):
        d = CountData(dataset=dataset.id, text=values.get('text'))
        d.create()
        return d

    @staticmethod
    def validate(dataset=None, values=None):
        return True

    def __init__(self, dataset, timestamp=None, text=None):
        self.dataset = dataset
        self.timestamp = timestamp
        self.text = text

    def __repr__(self):
        return "<CountData id:%s dataset.id:%s res_id:%s>" % (self.id, self.dataset,
            self.res_id)

class ValueData(db.Model):
    __tablename__ = "valuedata"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    dataset = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    text = db.Column(db.Text, nullable=True)

    value = db.Column(db.Float, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.res_id = next_res_id_for_data(ValueData, self.dataset)
        self.save()

    @staticmethod
    def from_values(dataset, values):
        d = ValueData(dataset=dataset.id, value=float(values.get('value')), text=values.get('text'))
        d.create()
        return d

    @staticmethod
    def validate(dataset=None, values=None):
        errors = {}
        if isinstance(values, dict):
            value = values.get('value')
            if value == None:
                errors['value'] = 'Value is required'
            else:
                try:
                    float(value)
                except ValueError:
                    errors['value'] = 'Invalid value'
        else:
            errors['value'] = 'Value is required'
        if errors == {}:
            return True
        else:
            return errors

    def __init__(self, dataset, timestamp=None, text=None, value=None):
        self.dataset = dataset
        self.timestamp = timestamp
        self.text = text
        self.value = value

    def __repr__(self):
        return "<ValueData id:%s dataset.id:%s res_id:%s>" % (self.id, self.dataset,
            self.res_id)

class TimedData(db.Model):
    __tablename__ = "timeddata"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    dataset = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    
    text = db.Column(db.Text, nullable=True)

    start = db.Column(db.DateTime, default=datetime.utcnow)
    stop = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.res_id = next_res_id_for_data(TimedData, self.dataset)
        self.save()

    @staticmethod
    def from_values(dataset, values):
        d = TimedData(dataset=dataset.id, start=ut_to_dt(int(values.get('start'))), stop=ut_to_dt(int(values.get('stop'))), text=values.get('text') )
        d.create()
        return d

    @staticmethod
    def validate(dataset=None, values=None):
        errors = {}
        if isinstance(values, dict):
            start, stop = values.get('start'), values.get('stop')
            if start == None:
                errors['start'] = 'Start is required'
            if stop == None:
                errors['stop'] = 'Stop is required'
            if start != None and stop != None:
                exception = False
                try:
                    int(start)
                except ValueError:
                    exception = True
                    errors['start'] = 'Invalid start'
                try:
                    int(stop)
                except ValueError:
                    exception = True
                    errors['stop'] = 'Invalid stop'
                if not exception:
                    if start > stop:
                        errors['stop'] = 'Stop must be greater than or equal to start'
        else:
            errors['start'] = 'Start is required'
            errors['stop'] = 'Stop is required'
        if errors == {}:
            return True
        else:
            return errors

    def __init__(self, dataset, text=None, start=None, stop=None):
        self.dataset = dataset
        self.start = start
        self.stop = stop
        self.text = text

    def __repr__(self):
        return "<TimedData id:%s dataset.id:%s res_id:%s>" % (self.id, self.dataset,
            self.res_id)


def next_res_id_for_choice(dataset):
    last = Choice.query.filter_by(dataset=dataset).order_by("-id").first()
    if last:
        return last.res_id + 1
    return 1

class Choice(db.Model):
    __tablename__ = "choice"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    dataset = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    title = db.Column(db.String(32))

    @staticmethod
    def for_dataset(dataset):
        return Choice.query.filter_by(dataset=dataset).all()

    @staticmethod
    def keys_for_dataset(dataset):
        choices = Choice.for_dataset(dataset)
        if choices != None:
            return [ (choice.res_id, choice.title) for choice in choices ]
        return []

    @staticmethod
    def list_for_dataset(dataset):
        choices = Choice.for_dataset(dataset)
        if choices != None:
            return [ choice.res_id for choice in choices ]
        return []

    @staticmethod
    def get(id):
        Choice.query.get(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.res_id = next_res_id_for_choice(self.dataset)
        self.save()

    def __init__(self, dataset, title):
        self.dataset = dataset
        self.title = title

    def __repr__(self):
        return "<Choice id:%s dataset.id:%s res_id:%s title:%s>" % (self.id,
            self.dataset, self.res_id, self.title)


class ChoiceData(db.Model):
    __tablename__ = "choicedata"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    dataset = db.Column(db.Integer, db.ForeignKey('dataset.id'))

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    text = db.Column(db.Text, nullable=True)

    # will hold the res_id
    choice = db.Column(db.Integer)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.res_id = next_res_id_for_data(ChoiceData, self.dataset)
        self.save()

    @staticmethod
    def from_values(dataset, values):
        d = ChoiceData(dataset=dataset.id, choice=int(values.get('choice')), text=values.get('text'))
        d.create()
        return d

    @staticmethod
    def validate(dataset=None, values=None):
        errors = {}
        if isinstance(values, dict):
            choice = values.get('choice')
            if choice == None:
                errors['choice'] = 'Choice is required'
            else:
                try:
                    choice = int(choice)
                    if choice not in Choice.list_for_dataset(dataset.id):
                        errors['choice'] = 'Invalid choice'
                except ValueError:
                    errors['choice'] = 'Invalid choice'
        else:
            errors['choice'] = 'Choice is required'
        if errors == {}:
            return True
        else:
            return errors

    def __init__(self, dataset, choice, timestamp=None, text=None):
        self.dataset = dataset
        self.choice = choice
        self.timestamp = timestamp
        self.text = text

    def __repr__(self):
        return "<ChoiceData id:%s dataset.id:%s res_id:%s>" % (self.id, self.dataset,
            self.res_id)

DATA_TYPE_CLASS = {
    1: CountData,
    2: ValueData,
    3: TimedData,
    4: ChoiceData
}

# each dataset should have relative resource ids (relative to collection)
def next_res_id_for_dataset(user):
    last = Dataset.query.filter_by(user=user).order_by("-id").first()
    if last:
        return last.res_id + 1
    return 1

def data_model_from_data_type(data_type):
    if data_type == DATA_TYPE_INT["count"]:
        return CountData
    elif data_type == DATA_TYPE_INT["value"]:
        return ValueData
    elif data_type == DATA_TYPE_INT["timed"]:
        return TimedData
    elif data_type == DATA_TYPE_INT["choice"]:
        return ChoiceData
    return None

class Dataset(db.Model):
    __tablename__ = "dataset"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    permissions_view = db.Column(db.Integer)
    res_id = db.Column(db.Integer)
    data_type = db.Column(db.Integer)

    unit_short = db.Column(db.String(12))
    unit = db.Column(db.String(32))

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    title = db.Column(db.Text)
    text = db.Column(db.Text, nullable=True)

    def data_type_str(self):
        return DATA_TYPE_INT_STR[self.data_type]

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.res_id = next_res_id_for_dataset(self.user)
        self.save()

    def get_data_with_res_id(self, res_id):
        mdl = data_model_from_data_type(self.data_type)
        return mdl.query.filter_by(dataset=self.id).filter_by(res_id=res_id).first()

    def get_data_all(self):
        mdl = data_model_from_data_type(self.data_type)
        return mdl.query.filter_by(dataset=self.id).all()

    def get_data_count(self):
        mdl = data_model_from_data_type(self.data_type)
        return mdl.query.filter_by(dataset=self.id).count()

    @staticmethod
    def from_values(user, values):
        title, text, data_type, unit, unit_short, choice_keys = values.get('title'), values.get('text'), int(values.get('data_type')), values.get('unit'), values.get('unit_short'), values.get('choice_keys')
        s = Dataset(user=user.id, title=title, data_type=data_type, text=text, unit=unit, unit_short=unit_short)
        s.create()
        if data_type == DATA_TYPE_INT['choice']:
            for key in choice_keys:
                Choice(dataset=s.id, title=key).create()
        return s


    @staticmethod
    def validate(values=None):
        errors = {}
        if isinstance(values, dict):
            title, data_type, unit, unit_short = values.get('title'), values.get('data_type'), values.get('unit'), values.get('unit_short')
            if title == None:
                errors['title'] = 'Title is required'
            elif re.search(VALID_TITLE_RE, title) == None:
                errors['title'] = 'Invalid title'
            if data_type == None:
                 errors['data_type'] = 'Data type is required'
            else:
                try:
                    data_type = int(data_type)
                    if data_type not in DATA_TYPE_STR:
                        errors['data_type'] = 'Invalid data type'
                    if data_type == DATA_TYPE_INT['choice']:
                        choice_keys = values.get('choice_keys')
                        if choice_keys == None:
                            errors['choice_keys'] = 'Choice dataset requires choice keys'
                        else:
                            if isinstance(choice_keys, list):
                                choice_errors = False
                                for key in choice_keys:
                                    try:
                                        str(key)
                                    except ValueError:
                                        choice_errors = True
                                if choice_errors:
                                    errors['choice_keys'] = 'One or more choices is invalid'
                            else:
                                errors['choice_keys'] = 'Choice keys must be in an array'
                except ValueError:
                    errors['data_type'] = 'Invalid data type'
            if unit != None:
                if re.search(VALID_TITLE_RE, unit) == None:
                    errors['unit'] = 'Invalid unit'
            if unit_short != None:
                if re.search(VALID_UNIT_SHORT_RE, unit_short) == None:
                    errors['unit_short'] = 'Invalid unit abbreviation'
        else:
            errors['title'] = 'Title is required'
            errors['data_type'] = 'Data type is required'
        if errors == {}:
            return True
        else:
            return errors

    def __init__(self, user, data_type, title, timestamp=None,
            text=None, unit=None, unit_short=None):
        self.user = user
        self.data_type = data_type
        self.title = title
        self.timestamp = timestamp
        self.text = text
        self.unit = unit
        self.unit_short = unit_short

    def __repr__(self):
        return "<Dataset id:%s user.id:%s res_id:%s data_type:%s>" % (self.id, 
            self.user, self.res_id, DATA_TYPE_STR[self.data_type])