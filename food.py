from google.appengine.ext import ndb

class User(ndb.Model):
    name = ndb.StringProperty()

class Food(ndb.Model):
    foodname = ndb.StringProperty()
    date = ndb.DateProperty()
    month = ndb.IntegerProperty()
    year = ndb.IntegerProperty()
    day = ndb.IntegerProperty()
    user_key = ndb.KeyProperty(User)
