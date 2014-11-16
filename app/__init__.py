from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
app.secret_key=app.config['SECRET_KEY']


from app import views

#login system
# import os
# from flask.ext.login import LoginManager
# from flask.ext.openid import OpenID
# from config import basedir

# lm = LoginManager()
# lm.init_app(app)
# oid = OpenID(app, os.path.join(basedir, 'tmp'))