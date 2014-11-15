from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config.from_object('config')


from app import views, models

#login system
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir

# lm = LoginManager()
# lm.init_app(app)
# oid = OpenID(app, os.path.join(basedir, 'tmp'))