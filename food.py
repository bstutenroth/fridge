from google.appengine.ext import ndb

class Food(ndb.Model):
    name = ndb.StringProperty()
    category = ndb.StringProperty()
    expirationdate = ndb.DateProperty()
