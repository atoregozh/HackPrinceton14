from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app
from db_model import City, User, db, Weather
from sqlalchemy import and_
import datetime
from twilio.rest import TwilioRestClient
# private settings
import keys

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
	if user == None:
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
				w.append({'class':'today', 'filename': weather.image_id, 'text':text})
			else:
				w.append({'class':'not-today','filename': weather.image_id, 'text':text})

	
	#retrieve user data from database
	session['username'] = username
	session['city'] = city.name
	# session['weathers'] = w=
	return render_template("loggedin.html", weathers = w)

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





