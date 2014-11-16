from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app
from db_model import City, User, db, Weather,Image
from sqlalchemy import and_
import datetime
# from forms import LoginForm
# from models import User

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


