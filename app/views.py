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
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)

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
	weathers_res = Weather.query.filter_by(city=city.name).all()
	w = []
	for weather in weathers_res:
		if (weather.timestamp.date() >= two_min) & (weather.timestamp.date() <= two_plus):
			w.append({'class':'xyz', 'filename': weather.image_id})
	print w

	
	#retrieve user data from database
	session['username'] = username
	session['city'] = city.name
	# session['weathers'] = w

	return render_template("loggedin.html", weathers = w)


# @app.route('/login', methods=['GET', 'POST'])
# @oid.loginhandler
# def login():
#     if g.user is not None and g.user.is_authenticated():
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         session['remember_me'] = form.remember_me.data
#         return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
#     return render_template('login.html', 
#                            title='Sign In',
#                            form=form,
#                            providers=app.config['OPENID_PROVIDERS'])