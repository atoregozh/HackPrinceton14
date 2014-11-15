from db_model import City, User, db, Weather
import datetime


boston = City('Boston,US')
admin = User('atoregozh', 'aizhan12345','F','+15108497098','Boston,US')
guest = User('atoregozh2', 'aizhan123456','M','+15108497098','Chapel Hill,US')

db.session.add(admin)
db.session.add(guest)
db.session.add(boston)
db.session.commit()

rain = Weather('Boston,US', 'clear', 'sky is clear', 3.86, timestamp=datetime.datetime.utcnow(),'01d')
db.session.add(rain)
db.session.commit()
weathers = Weather.query.all()
print weathers

users = User.query.all()
print users

cities = City.query.all()
print cities
