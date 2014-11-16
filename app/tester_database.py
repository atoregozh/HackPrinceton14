from db_model import City, User, db, Weather,Image
import datetime


boston = City('Boston,US')
admin = User('atoregozh5', 'aizhan12345','F','+15108497098','Boston,US')
guest = User('atoregozh6', 'aizhan123456','M','+15108497098','Chapel Hill,US')

db.session.add(admin)
db.session.add(guest)
db.session.commit()
users = User.query.all()
print users

db.session.add(boston)
db.session.commit()
cities = City.query.all()
print cities

now = datetime.datetime.utcnow()
# print now
# print now + datetime.timedelta(days=1)
# print now - datetime.timedelta(days=1)
w1 = Weather('Boston,US', 'clear', 'sky is clear', 3.86, now,'01d')
w2 = Weather('Boston,US', 'clear', 'sky is clear', 3.86, now - datetime.timedelta(days=1),'01d')
w3 = Weather('Boston,US', 'clear', 'sky is clear', 3.86, now + datetime.timedelta(days=1),'01d')
w4 = Weather('Boston,US', 'clear', 'sky is clear', 3.86, now + datetime.timedelta(days=2),'01d')
w5 = Weather('Boston,US', 'clear', 'sky is clear', 3.86, now - datetime.timedelta(days=2),'01d')

db.session.add(w1)
db.session.add(w2)
db.session.add(w3)
db.session.add(w4)
db.session.add(w5)
db.session.commit()
weathers = Weather.query.all()
print weathers

# pic = Image()

# cities = City.query.all()
# print cities
