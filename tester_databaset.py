from db_model import City, User, db, Weather,Image
import datetime


boston = City('Boston,US')
admin = User('atoregozh', 'aizhan12345','F','+15108497098','Boston,US')
guest = User('atoregozh2', 'aizhan123456','M','+15108497098','Chapel Hill,US')

db.session.add(admin)
db.session.add(guest)
db.session.commit()
users = User.query.all()
print users

db.session.add(boston)
db.session.commit()
cities = City.query.all()
print cities

rain = Weather('Boston,US', 'clear', 'sky is clear', 3.86, datetime.datetime.utcnow(),'01d')
db.session.add(rain)
db.session.commit()
weathers = Weather.query.all()
print weathers

pic = Image()

cities = City.query.all()
print cities
