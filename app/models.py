from app import db, secret
from datetime import datetime
import os, binascii, hashlib

'''
   it is VERY important that the resources are saved immediately, otherwise the
   res_id won't work properly and there will be collisions.  The res_id is so
   that each resource will have an id relative to that owner or set.  For example,
   we want the following url user/jim/valueset/1/1 referring to the valuedata
   1 for valueset 1, INSTEAD OF user/jim/valueset/839/10425.  The first uses a
   relative id, and the second uses an absolute row/pk id.  Using rel_id the URL id
   will refer only to that set or owner, so there can be a user/jim/valueset/2/1, etc.
'''

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True)
    salt = db.Column(db.String(6))
    password = db.Column(db.String(64))

    def __init__(self, username, password):
        self.username = username
        self.salt = User.create_salt()
        self.password = self.hash_password(password)

    @staticmethod
    def create_salt():
        return binascii.b2a_hex(os.urandom(3))

    def hash_password(self, pswd):
        return hashlib.sha256(pswd + self.salt + secret).hexdigest()

    def matches_password(self, str):
        return self.password == self.hash_password(str)

class TimePoint(db.Model):
    __tablename__ = "timepoint"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)

    def __init__(self, timestamp=datetime.now(), text=None):
        self.timestamp = timestamp
        self.text = text

def res_set_count(model, set):
    return model.query.filter_by(set=set).count()

class CountData(db.Model):
    __tablename__ = "countdata"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    set = db.Column(db.Integer, db.ForeignKey('countset.id'))

    timestamp = db.Column(db.DateTime)
    
    text = db.Column(db.Text, nullable=True)

    def __init__(self, set, timestamp=datetime.now(), text=None):
        self.set = set
        self.timestamp = timestamp
        self.text = text
        self.res_id = res_set_count(TimedData, set)

class ValueData(db.Model):
    __tablename__ = "valuedata"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    set = db.Column(db.Integer, db.ForeignKey('valueset.id'))
    
    timestamp = db.Column(db.DateTime)

    text = db.Column(db.Text, nullable=True)

    value = db.Column(db.Float, nullable=True)

    def __init__(self, set, timestamp=datetime.now(), text=None, value=None):
        self.set = set
        self.timestamp = timestamp
        self.text = text
        self.value = value
        self.res_id = res_set_count(TimedData, set)

class TimedData(db.Model):
    __tablename__ = "timeddata"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    set = db.Column(db.Integer, db.ForeignKey('timedset.id'))
    
    text = db.Column(db.Text, nullable=True)

    start = db.Column(db.Integer, db.ForeignKey('timepoint.id'), nullable=True)
    stop = db.Column(db.Integer, db.ForeignKey('timepoint.id'), nullable=True)

    def __init__(self, set, text=None, start=None, stop=None):
        self.set = set
        self.start = start
        self.stop = stop
        self.text = text
        self.res_id = res_set_count(TimedData, set)

def res_owner_count(model, owner):
    return model.query.filter_by(owner=owner).count()

class CountSet(db.Model):
    __tablename__ = "countset"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    timestamp = db.Column(db.DateTime)

    title = db.Column(db.Text)
    text = db.Column(db.Text, nullable=True)

    def __init__(self, owner, title, timestamp=datetime.now(), text=None):
        self.owner = owner
        self.title = title
        self.timestamp = timestamp
        self.text = text
        self.res_id = res_owner_count(CountSet, owner) + 1

class ValueSet(db.Model):
    __tablename__ = "valueset"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    timestamp = db.Column(db.DateTime)

    title = db.Column(db.Text)
    text = db.Column(db.Text, nullable=True)

    def __init__(self, owner, title, timestamp=datetime.now(), text=None):
        self.owner = owner
        self.title = title
        self.timestamp = timestamp
        self.text = text
        self.res_id = res_owner_count(ValueSet, owner) + 1

class TimedSet(db.Model):
    __tablename__ = "timedset"
    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    timestamp = db.Column(db.DateTime)

    title = db.Column(db.Text)
    text = db.Column(db.Text, nullable=True)

    def __init__(self, owner, title, timestamp=datetime.now(), text=None):
        self.owner = owner
        self.title = title
        self.timestamp = timestamp
        self.text = text
        self.res_id = res_owner_count(TimedSet, owner) + 1