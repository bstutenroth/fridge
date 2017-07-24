from google.appengine.ext import ndb

class User(ndb.Model):
    name = ndb.StringProperty()

class Food(ndb.Model):
    foodname = ndb.StringProperty()
    expire_date = ndb.DateTimeProperty()
    user_key = ndb.KeyProperty(User)
