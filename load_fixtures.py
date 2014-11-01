from app import app, db
from app.models import *
from random import randrange
from time import sleep

db.create_all()

usr = User('foo', 'pswd')
usr.create()

rcrd = Record(1, 'First Record')
rcrd.create()

cset = Set(1, 1, 'First Count Set')
cset.create()

vset = Set(1, 2, 'First Value Set')
vset.create()

tset = Set(1, 3, 'First Timed Set')
tset.create()

cset2 = Set(1, 1, 'Second Count Set')
cset2.create()

'''
from app.models import *
from app.serializers import *
u = User.query.get(1)
user(u)
r = Record.query.get(1)
record(r)
s = r.get_set_with_res_id(1)
set(s)


from app.models import *
from app.serializers import *

r = Record.query.get(1)
record(r)

s = r.get_set_with_res_id(1)

set(s)




'''





for i in range(10):
    rand = randrange(0,4)
    print "sleep %d" % rand
    sleep(rand)
    cdata = CountData(1)
    cdata.create()