from app import db, secret
from datetime import datetime
import os, binascii, hashlib

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True)
    password = db.Column(db.String(64))
    salt = db.Column(db.String(64))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.save()

    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)
        self.salt = User.create_salt()

    def __repr__(self):
        return "<User id:%d>" % self.id

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
def next_res_id_for_set(mdl, record):
    last = db.session.query(mdl).filter_by(record=record).order_by("-id").first()
    if last:
        return last.res_id + 1
    return 1

class CountSet(db.Model):
    __tablename__ = "countset"
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
        self.res_id = next_res_id_for_set(CountSet, self.record)
        self.save()

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

    record = db.Column(db.Integer, db.ForeignKey('record.id'))

    timestamp = db.Column(db.DateTime)

    title = db.Column(db.Text)
    text = db.Column(db.Text, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.res_id = next_res_id_for_set(ValueSet, self.record)
        self.save()

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
        self.res_id = next_res_id_for_set(TimedSet, self.record)
        self.save()

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

    timestamp = db.Column(db.DateTime)

    title = db.Column(db.Text)
    text = db.Column(db.Text, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self):
        self.res_id = next_res_id_for_record(Record, self.owner)
        self.save()

    def __init__(self, owner, title, timestamp=datetime.now(), text=None):
        self.owner = owner
        self.title = title
        self.timestamp = timestamp
        self.text = text

    def __repr__(self):
        return "<Record id:%d owner.id:%d>" % (self.id, self.owner)
