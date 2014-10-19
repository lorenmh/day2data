from app import app, db
from app.models import *

db.create_all()

usr = User('foo', 'pswd')
usr.save()
usr = User('foo2', 'pswd')
usr.save()
cset = CountSet(1, 'First Count Set')
cset.save()
cset = CountSet(1, 'second Count Set')
cset.save()
cset = CountSet(1, 'third Count Set')
cset.save()
cset = CountSet(1, 'fourth Count Set')
cset.save()
cset = CountSet(2, 'fifth Count Set')
cset.save()
cset = CountSet(2, 'sixth Count Set')
cset.save()