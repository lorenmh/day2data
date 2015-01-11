### Installation:
Make sure postgres is installed.

make a virtualenv named env:
```virtualenv env```

use this virtualenv:
```. src```

install redis and postgres
**Note: the app uses the default redis / postgres ports**

install python depends:
```pip install -r requirements.txt```

if there are errors, make sure to install system things like python-dev, postgres, etc.

install node / nodejs:
```sudo apt-get install nodejs``` or ```brew install node```
```sudo apt-get install npm```

install bower and gulp as global:
```sudo npm install -g gulp```
```sudo npm install -g bower```

create a postgres user and db:
```
sudo su - postgres
psql
CREATE ROLE owner_name WITH LOGIN PASSWORD 'some_password';
CREATE DATABASE db_name WITH OWNER owner_name;
```

In the parent directory of wherever this repo is install, create a 'vars' directory:
```mkdir ../vars```

put a d2d.py file in there:
```
touch ../vars/d2d.py
touch ../__init__.py
touch ../vars/__init__.py

```

this d2d.py file should have a 'vars' dict with the keys 'DB_URI', 'SECRET', 'SECRET_KEY':
```
# in ../vars/d2d.py
vars = {
    'DB_URI': 'postgres://owner_name:some_password@localhost/db_name',
    'SECRET_KEY': 'some secret',
    'SECRET': 'some secret'
}
```

install the bower libs in the repo directory:
```bower install```

build the front end assets:
```gulp all```

initialize the flask models:
```python load_fixtures()```

start the redis server:
```sudo redis-server```

start the server:
```./server```

everything should be running now
