from app import app, db
from app.models import *
from random import randrange
from time import sleep

db.create_all()

usr = User('foo', 'pswd')
usr.create()

col = Collection(1, 'First Record')
col.create()

cset = DataSet(1, 1, 'First Count Set')
cset.create()
'''
vset = Set(1, 2, 'First Value Set')
vset.create()

tset = Set(1, 3, 'First Timed Set')
tset.create()

chset = Set(1, 4, 'First Choice Set')
chset.create()
chset2 = Set(1, 4, 'Second Choice Set')
chset2.create()

cset2 = Set(1, 1, 'Second Count Set')
cset2.create()

ch1 = Choice(4, "Red light")
ch1.create()
ch2 = Choice(4, "Yellow light")
ch2.create()
ch3 = Choice(4, "Green light")
ch3.create()

ch4 = Choice(5, "Cloudy")
ch4.create()
ch5 = Choice(5, "Sunny")
ch5.create()
ch6 = Choice(5, "Rainy")
ch6.create()
ch7 = Choice(5, "Windy")
ch7.create()

for i in range(10):
    rand = randrange(1, 4)
    ch_data = ChoiceData(4, rand)
    ch_data.create()

for i in range(10):
    rand = randrange(1, 5)
    ch_data = ChoiceData(5, rand)
    ch_data.create()
'''
# the lazy haha
for i in range(4):
    rand = randrange(0,6)
    print "sleep %d" % rand
    sleep(rand)
    cdata = CountData(1)
    cdata.create()