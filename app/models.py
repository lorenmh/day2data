from app import db, secret
from datetime import datetime
import os, binascii, hashlib, re

VALID_PSWD_RE = "^[\w\!\@\#\$\%\^\&\*\-]{4,32}$"
VALID_USERNAME_RE = "^[\w\-]{3,16}$"
VALID_UNIT_RE = "^[\w\!\(\)\-\+\[\]\,\/\#\$\%\&\*\€\£\.]{1,10}$"

PERMISSIONS_VIEW = {
    "private": 1,
    "public": 2
}

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(64))
    salt = db.Column(db.String(64))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.save()

    def get_record_with_res_id(self, res_id):
        return Record.query.filter_by(owner=self.id).filter_by(res_id=res_id).first()

    def get_record_all(self):
        return Record.query.filter_by(set=self.id).all()

    def __init__(self, username, password):
        self.username = username
        self.salt = User.create_salt()
        self.password = self.hash_password(password)

    def __repr__(self):
        return "<User id:%d>" % self.id

    @staticmethod
    def with_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def valid_password(pswd):
        return re.match(VALID_PSWD_RE, pswd) != None

    @staticmethod
    def valid_username(username):
        return re.match(VALID_USERNAME_RE, username) != None

    @staticmethod
    def create_salt():
        return binascii.b2a_hex(os.urandom(32))

    def hash_password(self, pswd):
        return hashlib.sha256(pswd + self.salt + secret).hexdigest()

    def matches_password(self, str):
        return self.password == self.hash_password(str)

class TimePoint(db.Model):
    __tablename__ = "timepoint"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.save()

    def __init__(self, timestamp=datetime.now(), text=None):
        self.timestamp = timestamp
        self.text = text

    def __repr__(self):
        return "<TimePoint id:%d>" % self.id

# finds the current max res_id for this set
def next_res_id_for_data(mdl, set):
    last = db.session.query(mdl).filter_by(set=set).order_by("-id").first()
    if last:
        return last.res_id + 1
    return 1

class CountData(db.Model):
    __tablename__ = "countdata"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    set = db.Column(db.Integer, db.ForeignKey('countset.id'))

    timestamp = db.Column(db.DateTime)
    
    text = db.Column(db.Text, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.res_id = next_res_id_for_data(CountData, self.set)
        self.save()

    def __init__(self, set, timestamp=datetime.now(), text=None):
        self.set = set
        self.timestamp = timestamp
        self.text = text

    def __repr__(self):
        return "<CountData id:%d countset.id:%d>" % (self.id, self.set)

class ValueData(db.Model):
    __tablename__ = "valuedata"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    set = db.Column(db.Integer, db.ForeignKey('valueset.id'))
    
    timestamp = db.Column(db.DateTime)

    text = db.Column(db.Text, nullable=True)

    value = db.Column(db.Float, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.res_id = next_res_id_for_data(ValueData, self.set)
        self.save()

    def __init__(self, set, timestamp=datetime.now(), text=None, value=None):
        self.set = set
        self.timestamp = timestamp
        self.text = text
        self.value = value

    def __repr__(self):
        return "<ValueData id:%d valueset.id:%d>" % (self.id, self.set)

class TimedData(db.Model):
    __tablename__ = "timeddata"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    set = db.Column(db.Integer, db.ForeignKey('timedset.id'))
    
    text = db.Column(db.Text, nullable=True)

    start = db.Column(db.Integer, db.ForeignKey('timepoint.id'), nullable=True)
    stop = db.Column(db.Integer, db.ForeignKey('timepoint.id'), nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.res_id = next_res_id_for_data(TimedData, self.set)
        self.save()

    def __init__(self, set, text=None, start=None, stop=None):
        self.set = set
        self.start = start
        self.stop = stop
        self.text = text

    def __repr__(self):
        return "<TimedData id:%d timedset.id:%d>" % (self.id, self.set)

# each set should have relative resource ids (relative to record)
def next_res_id_for_set(record):
    cs = CountSet.query.filter_by(record=record).order_by('-id').first()
    vs = ValueSet.query.filter_by(record=record).order_by('-id').first()
    ts = TimedSet.query.filter_by(record=record).order_by('-id').first()
    lst = []
    if (cs != None):
        lst.append(cs.res_id)
    if (vs != None):
        lst.append(vs.res_id)
    if (ts != None):
        lst.append(ts.res_id)
    if (cs == None or vs == None or ts == None):
        lst.append(0)
    return max(lst) + 1

class CountSet(db.Model):
    __tablename__ = "countset"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer, nullable=True)
    record = db.Column(db.Integer, db.ForeignKey('record.id'))

    unit_short = db.Column(db.String(12))
    unit = db.Column(db.String(32))

    timestamp = db.Column(db.DateTime)

    title = db.Column(db.Text)
    text = db.Column(db.Text, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.res_id = next_res_id_for_set(self.record)
        self.save()

    def get_data_with_res_id(self, res_id):
        return CountData.query.filter_by(set=self.id).filter_by(res_id=res_id).first()

    def get_data_all(self):
        return CountData.query.filter_by(set=self.id).all()

    def __init__(self, record, title, timestamp=datetime.now(), text=None):
        self.record = record
        self.title = title
        self.timestamp = timestamp
        self.text = text

    def __repr__(self):
        return "<CountSet id:%d record.id:%d>" % (self.id, self.record)

class ValueSet(db.Model):
    __tablename__ = "valueset"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer, nullable=True)
    record = db.Column(db.Integer, db.ForeignKey('record.id'))

    timestamp = db.Column(db.DateTime)

    title = db.Column(db.Text)
    text = db.Column(db.Text, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.res_id = next_res_id_for_set(self.record)
        self.save()

    def get_data_with_res_id(self, res_id):
        return ValueData.query.filter_by(set=self.id).filter_by(res_id=res_id).first()

    def get_data_all(self):
        return ValueData.query.filter_by(set=self.id).all()

    def __init__(self, record, title, timestamp=datetime.now(), text=None):
        self.record = record
        self.title = title
        self.timestamp = timestamp
        self.text = text

    def __repr__(self):
        return "<ValueSet id:%d record.id:%d>" % (self.id, self.record)

class TimedSet(db.Model):
    __tablename__ = "timedset"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    record = db.Column(db.Integer, db.ForeignKey('record.id'))

    timestamp = db.Column(db.DateTime)

    title = db.Column(db.Text)
    text = db.Column(db.Text, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.res_id = next_res_id_for_set(self.record)
        self.save()

    def get_data_with_res_id(self, res_id):
        return TimedData.query.filter_by(set=self.id).filter_by(res_id=res_id).first()

    def get_data_all(self):
        return TimedData.query.filter_by(set=self.id).all()

    def __init__(self, record, title, timestamp=datetime.now(), text=None):
        self.record = record
        self.title = title
        self.timestamp = timestamp
        self.text = text

    def __repr__(self):
        return "<TimedSet id:%d record.id:%d>" % (self.id, self.record)

def next_res_id_for_record(mdl, owner):
    last = db.session.query(mdl).filter_by(owner=owner).order_by("-id").first()
    if last:
        return last.res_id + 1
    return 1

class Record(db.Model):
    __tablename__ = "record"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    permissions_view = db.Column(db.Integer)

    timestamp = db.Column(db.DateTime)

    title = db.Column(db.Text)
    text = db.Column(db.Text, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.res_id = next_res_id_for_record(Record, self.owner)
        self.save()

    def get_set_with_res_id(self, res_id):
        cs = CountSet.query.filter_by(record=self.id).filter_by(res_id=res_id).first()
        if cs:
            return cs
        vs = ValueSet.query.filter_by(record=self.id).filter_by(res_id=res_id).first()
        if vs:
            return vs
        ts = TimedSet.query.filter_by(record=self.id).filter_by(res_id=res_id).first()
        if ts:
            return ts
        return None

    def get_set_all(self):
        cs = CountSet.query.filter_by(record=self.id).all()
        vs = ValueSet.query.filter_by(record=self.id).all()
        ts = TimedSet.query.filter_by(record=self.id).all()
        lst = cs + vs + ts
        return sorted(lst, key = lambda model_instance : model_instance.res_id)

    def __init__(self, owner, title, permissions_view=PERMISSIONS_VIEW['private'],
            timestamp=datetime.now(), text=None):
        self.owner = owner
        self.title = title
        self.permissions_view = permissions_view
        self.timestamp = timestamp
        self.text = text

    def __repr__(self):
        return "<Record id:%d owner.id:%d>" % (self.id, self.owner)
