#!../bin/python
from app import app
#app.run(debug=True) #only allow connections from localhost
app.run(host='0.0.0.0') #enable external connections