import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import users
from food import User
from food import Food
import datetime


env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class HomeHandler(webapp2.RequestHandler):
    def get (self):
        user = users.get_current_user()
        if user:
            email = user.nickname()

            # current_user = User(user_id=email)
            greeting = ('<div class = "logout">Welcome, %s! (<a href="%s">sign out</a>)</div>' %
                (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<div class = "login" ><a href="%s">Sign in or register</a></div>' %
                users.create_login_url('/'))

        self.response.write('<html><body>%s</body></html>' % greeting)
        template = env.get_template('homepage.html')
        self.response.out.write(template.render())

class NewFoodHandler(webapp2.RequestHandler):
    def get (self):
        newfood_template = env.get_template('newfood.html')
        self.response.out.write(newfood_template.render())

#Adding New Food to Datastore
    def post(self):
        global user
        submitted_variables = {
            'foodname':self.request.get("foodname"),
            'category':self.request.get("category"),
            'month':self.request.get("month"),
            'year':self.request.get("year"),
            'day':self.request.get("day")
        }
        # brenna=User(name='brenna')
        # brenna_key=brenna.put()
        food1 = Food(user_key=user.key, foodname= submitted_variables['foodname'], month=int(submitted_variables['month']),year=int(submitted_variables['year']),day=int(submitted_variables['day']))
        food1_key=food1.put()

#Displaying on Calendar Handler
class ListofExpirationHandler(webapp2.RequestHandler):
    def get (self):
        # find who's the current user
        current_user = users.get_current_user()
        current_user_id = current_user.id()
        current_user_email = current_user.nickname()

        # make a query for the user whose email is current_user_emaul
        # my_user_query =
        # # fetch
        # my_user =

        #will use these two lines with datastore
        food_list = Food.query(Food.user_key == my_user.key).fetch()
        variables = {'food_list': food_list}

        #temp variable list to display on calendar while waiting on datastore
        # temp_food = [{'foodname':'Chicken', 'category':'Meat', 'expire_date':datetime.date(2017,8,1)},
        # {'foodname':'Milk', 'category':'Dairy', 'expire_date':datetime.date(2017,7,31)},
        # {'foodname':'Grapes', 'category':'Fruit', 'expire_date':datetime.date(2017,7,28)}]
        # temp_user = 'Brenna'

        #will attempt to sort temp items in temp_food by expire date
        temp_food.sort(key=lambda item:item['expire_date'], reverse=False)
        temp_variables = {'temp_user':temp_user, 'temp_food':temp_food}
        list_template = env.get_template('calendar.html')
        self.response.write(list_template.render(temp_variables))

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/newfood', NewFoodHandler),
    ('/calendar', ListofExpirationHandler)
], debug=True)
