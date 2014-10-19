from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os, sys

# import vars for d2d from vars directory
sys.path.append('../vars')
import d2d

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = d2d.vars['DB_URI']
db = SQLAlchemy(app)

secret = d2d.vars["SECRET"]
app.secret_key = d2d.vars["SECRET_KEY"]

from app import views
