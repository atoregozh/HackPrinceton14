from db_model import City, User, db, Weather,Image
import datetime


boston = City('Boston,US')
los_ang = City('Los Angeles,US')
princeton = City('Princeton,US')
chapel_hill = City('Chapel Hill,US')
florida = City('Florida,US')

u1 = User('atoregozh', 'aizhan12345','F','+15108497098','Los Angeles,US')
u2 = User('kesiena', 'kes123456','M','+15108497098','Chapel Hill,US')
u3 = User('kayla', 'kayla123456','M','+15108497098','Boston,US')
u4 = User('christie', 'cris123456','M','+15108497098','Florida,US')


db.session.add(u1)
db.session.add(u2)
db.session.add(u3)
db.session.add(u4)
db.session.commit()

users = User.query.all()
print users

db.session.add(boston)
db.session.add(los_ang)
db.session.add(princeton)
db.session.add(florida)
db.session.add(chapel_hill)
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

w6 = Weather('Florida,US', 'clear', 'sky is clear', 20.5, now,'01d')
w7 = Weather('Florida,US', 'clear', 'sky is clear', 15, now - datetime.timedelta(days=1),'03d')
w8 = Weather('Florida,US', 'clear', 'sky is clear', 5, now + datetime.timedelta(days=1),'09d')
w9 = Weather('Florida,US', 'clear', 'sky is clear', 3.2, now + datetime.timedelta(days=2),'11d')
w10 = Weather('Florida,US', 'clear', 'sky is clear', -4.5, now - datetime.timedelta(days=2),'13d')

db.session.add(w1)
db.session.add(w2)
db.session.add(w3)
db.session.add(w4)
db.session.add(w5)
db.session.add(w6)
db.session.add(w7)
db.session.add(w8)
db.session.add(w9)
db.session.add(w10)
db.session.commit()
weathers = Weather.query.all()
print weathers

# pic = Image()

# cities = City.query.all()
# print cities
