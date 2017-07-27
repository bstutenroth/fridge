from google.appengine.ext import ndb

class User(ndb.Model):
    email = ndb.StringProperty()
    consume = ndb.IntegerProperty()
    expire = ndb.IntegerProperty()    

class Food(ndb.Model):
    foodname = ndb.StringProperty()
    date = ndb.DateProperty()
    user_key = ndb.KeyProperty(User)
    category = ndb.StringProperty()
    # categories: Meat, Dairy, Drinks, Produce, Other
    #case sensitive
