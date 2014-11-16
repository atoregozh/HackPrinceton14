#!../../bin/python
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
		
#create database
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db') #app.db is the name of database
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True)
    password = db.Column(db.String(15))
    phone_num = db.Column(db.String(12))
    city = db.Column(db.String(40), db.ForeignKey('city.name'))


    def __init__(self, username, password, phone_num, city):
	    self.username = username
	    self.password = password
	    self.phone_num = phone_num
	    self.city = city

    def __repr__(self):
        return '<User %r>' % (self.username)

class City(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), index=True, unique=True)
    weather = db.relationship('Weather', backref = 'weather_city', lazy='dynamic')
    user = db.relationship('User', backref = 'user_city', lazy='dynamic')

    def __init__(self, name):
    	self.name = name

    def __repr__(self):
        return '<City %r>' % (self.name)


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    city = db.Column(db.String(40), db.ForeignKey('city.name'))
    category = db.Column(db.String(30))
    cat_desc = db.Column(db.String(140))
    temperature = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)
    image_id = db.Column(db.String(5))   

    def __init__(self, city, category, cat_desc, temperature, timestamp, image_id):
	    self.city = city
	    self.category = category
	    self.cat_desc = cat_desc
	    self.temperature = temperature
	    self.timestamp = timestamp
	    self.image_id = image_id

    def __repr__(self):
        return '<Weather %r>' % (self.cat_desc)

# class Image(db.Model):
#     id = db.Column(db.Integer(), primary_key = True)
#     img_id = db.Column(db.String(5), unique=True)
#     weather = db.relationship('Weather', backref = 'image', lazy='dynamic')
#     url = db.Column(db.String(140))

#     def __init__(self,img_id,url):
#         self.img_id = img_id
# 	    self.url = url

#     def __repr__(self):
# 	    return '<Image %r>' % (self.id)


