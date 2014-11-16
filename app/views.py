from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app
from db_model import City, User, db, Weather
from sqlalchemy import and_
import datetime, urllib2, json
from twilio.rest import TwilioRestClient
# private settings
import keys
import sys

img_weather = {'01d': "http://media-cache-ec0.pinimg.com/236x/3e/21/89/3e2189ba8571cf72e0e08ffa2ae5523f.jpg",
				'01n': "http://media-cache-ec0.pinimg.com/236x/3e/21/89/3e2189ba8571cf72e0e08ffa2ae5523f.jpg",
				'02d': "http://media-cache-ec0.pinimg.com/236x/3e/21/89/3e2189ba8571cf72e0e08ffa2ae5523f.jpg",
				'02n': "http://media-cache-ec0.pinimg.com/236x/3e/21/89/3e2189ba8571cf72e0e08ffa2ae5523f.jpg",
				'03d' : "http://www.jokeoverflow.com/wp-content/uploads/2012/12/21795_546818308665550_720643909_n.jpg",
				'03n' : "http://www.jokeoverflow.com/wp-content/uploads/2012/12/21795_546818308665550_720643909_n.jpg",
				'04d' : "http://www.jokeoverflow.com/wp-content/uploads/2012/12/21795_546818308665550_720643909_n.jpg",
				'04n' : "http://www.jokeoverflow.com/wp-content/uploads/2012/12/21795_546818308665550_720643909_n.jpg",
				'09d' : "http://www.jokeoverflow.com/wp-content/uploads/2012/12/21795_546818308665550_720643909_n.jpg",
				'09n' : "http://www.jokeoverflow.com/wp-content/uploads/2012/12/21795_546818308665550_720643909_n.jpg"}


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title='Wthr')

@app.route('/login', methods=['POST'])
def login():
	username = request.form['username']
	password = request.form['password']
	
	#authenticated user
	user = User.query.filter_by(username=username).first()
	if user is None:
		return render_template("index.html")
	user_id = user.id

	# xxxxxxxxx
	if username == "kesiena":
		send_mms()
	# xxxxxxxxx

	#set user ID in session
	session['user_id'] = user_id

	city = City.query.filter_by(name=user.city).first()
	now = datetime.datetime.utcnow().date()
	two_min = now - datetime.timedelta(days=2)
	two_plus = now + datetime.timedelta(days=2)

	#query all weathers for the city and then subset
	weathers_res = Weather.query.filter_by(city=city.name).order_by(Weather.timestamp.desc()).all()
	w = []
	for weather in weathers_res:
		wd = weather.timestamp.date()
		text =  ("%s %s" % (weather.timestamp.strftime('%a'), weather.temperature))
		if (wd >= two_min) & (wd <= two_plus):
			if (wd == now):
				session['bigImgUrl'] = img_weather[weather.image_id]
				w.append({'class':'today-forecast-div', 'filename': weather.image_id, 'text':text})
			else:
				w.append({'class':'forecast-div','filename': weather.image_id, 'text':text})

	
	#retrieve user data from database
	session['username'] = username
	session['city'] = city.name
	# session['weathers'] = w=
	return render_template("loggedin.html", weathers = w)

@app.route('/register', methods=['POST'])
def register():
	username = request.form['username']
	password = request.form['password']
	city = request.form['city']
	phone = request.form['phone']

	#city exists
	db_city = City.query.filter_by(name=city).first()
	#if city dne, then create in db
	if db_city is None:
		put_city(city)
		db_city = City.query.filter_by(name=city).first()

	u1 = User(username, password, phone,city)
	db.session.add(u1)
	db.session.commit()
	db_user = User.query.filter_by(username=username).first()

	session['user_id'] = db_user.id
	session['username'] = username
	session['city'] = db_city.name

	now = datetime.datetime.utcnow().date()
	two_min = now - datetime.timedelta(days=2)
	two_plus = now + datetime.timedelta(days=2)
	#query all weathers for the city and then subset
	weathers_res = Weather.query.filter_by(city=db_city.name).order_by(Weather.timestamp.desc()).all()
	w = []
	for weather in weathers_res:
		wd = weather.timestamp.date()
		text =  ("%s %s" % (weather.timestamp.strftime('%a'), weather.temperature))
		if (wd >= two_min) & (wd <= two_plus):
			if (wd == now):
				session['bigImgUrl'] = img_weather[weather.image_id]
				w.append({'class':'today-forecast-div', 'filename': weather.image_id, 'text':text})
			else:
				w.append({'class':'forecast-div','filename': weather.image_id, 'text':text})

	return render_template("loggedin.html", weathers = w)

def put_city(city_name):
  city_obj = City(city_name)
  db.session.add(city_obj)
  d = datetime.datetime.utcnow() - datetime.timedelta(days=2)
  while d <= datetime.datetime.utcnow() + datetime.timedelta(days=2):
    #w = Weather(city_name, 'clear', 'sky is clear', 3.86, d,'01d')
    w2 = json.loads(get_weather(city_name, d))
    temp = w2['list'][0]['temp']['day']
    weat = w2['list'][0]['weather']
    iconId = weat[0]['icon']
    category = weat[0]['main']
    desc = weat[0]['description']
    w = Weather(city_name, category, desc, temp, d,iconId)
    db.session.add(w)
    d = d + datetime.timedelta(days=1)
  db.session.commit()

@app.route('/logout')
def logout():
	return render_template("index.html",
                           title='Wthr')

# @app.route('/send_mms', methods=['POST'])
def send_mms():
    account_sid = keys.twilio_id
    auth_token  = keys.twilio_token
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(body="Today is fucking snowing!", 
           to="+15108497098",
           from_="+15104471209",
           media_url="http://i.qkme.me/3tf0y8.jpg")

def get_weather(city, date):
  uri = ("http://api.openweathermap.org/data/2.5/forecast/daily?q=%s&mode=json&units=metric&type=hour&start=%s&cnt=1&APPID=bd6a2021af827442a3011948d0101ef7" % (city, date))
  return urllib2.urlopen(uri).read()
  