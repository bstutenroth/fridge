from google.appengine.ext import ndb

class Food(ndb.Model):
    name = ndb.StringProperty()
    foodname = ndb.StringProperty()
    expire_date = ndb.DateTimeProperty()
