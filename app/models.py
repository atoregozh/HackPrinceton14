from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True)
    password = db.Column(db.String(15))
    sex = db.Column(db.String(1), unique=True)
    phone_num = db.Column(db.String(12))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))


    def __init__(self, username, password, sex, phone_num, city_id):
	    self.username = username
	    self.password = password
	    self.sex = sex
	    self.phone_num = phone_num
	    self.city_id = city_id

    def __repr__(self):
        return '<User %r>' % (self.username)

class City(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    city_name = db.Column(db.String(140), index=True, unique=True)
    weathers = db.relationship('Weather', backref = 'city', lazy='dynamic')
    user = db.relationship('User', backref = 'city', lazy='dynamic')

    def __init__(self, city_name):
    	self.city_name = city_name

    def __repr__(self):
        return '<City %r>' % (self.city_name)


class Weather(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	category = db.Column(db.String(30))
	cat_desc = db.Column(db.String(140))
	city_name = db.Column(db.Integer, db.ForeignKey('city.city_name'))
	image_id = db.Column(db.String(5), db.ForeignKey('image.id'))
	timestamp = db.Column(db.DateTime)
	temperature = db.Column(db.Float)


	def __init__(self, city_name, category, cat_desc, temperature, timestamp, image_id):
		self.city_name = city_name
		self.category = category
		self.cat_desc = cat_desc
		self.temperature = temperature
		self.timestamp = timestamp
		self.image_id = image_id

	def __repr__(self):
        return '<Weather %r>' % (self.cat_desc)

class Image(db.Model):
	id = db.Column(db.String(5), primary_key = True)
	picture = db.Column(db.LargeBinary)
	weather = db.relationship('Weather', backref = 'image', lazy='dynamic')

	def __init__(self,picture, weather):
		self.weather = weather
		self.picture = picture

	def __repr__(self):
		return '<Image %r>' % (self.id)

	

		

