import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import users
from food import User
from food import Food
from datetime import datetime


env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class HomeHandler(webapp2.RequestHandler):
    def get (self):
        user = users.get_current_user()
        if user:
            greeting = ('<div class = "logout">Welcome, %s! (<a href="%s">sign out</a>)</div>' %
                (user.nickname(), users.create_logout_url('/')))
            all_users_query = User.query()
            all_users = all_users_query.fetch()
            print user.nickname()
            print all_users
            # for get_user in all_users:
            #     if user.nickname() != get_user.email
            #         pass
            #     if else:
            #         new_user = User(email=user.nickname())
            #         new_user.put()
            #         all_users_query = User.query()
            #         all_users = all_users_query.fetch()
            #         print all_users
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
        submitted_variables = {
            'foodname':self.request.get("foodname"),
            'category':self.request.get("category"),
            #'month':self.request.get("month"),
            #'year':self.request.get("year"),
            #'day':self.request.get("day"),
            'date':self.request.get('expiredate')
        }
        brenna=User(name='brenna')
        brenna_key=brenna.put()
        food1 = Food(user_key=brenna_key, foodname= submitted_variables['foodname'], date=datetime.strptime(submitted_variables['date'], '%Y-%m-%d'))
        food1_key=food1.put()

#Displaying on Calendar Handler
class ListofExpirationHandler(webapp2.RequestHandler):
    def get (self):
        # find who's the current user
        # current_user = users.get_current_user()
        # current_user_id = current_user.id()
        # current_user_email = current_user.nickname()

        # make a query for the user whose email is current_user_emaul
        # my_user_query =
        # # fetch
        # my_user =

        # #will use these two lines with datastore
        brenna=User(name='brenna')
        brenna_key=brenna.put()
        food_list = Food.query().fetch()
        variables = {'food_list': food_list}

        #temp variable list to display on calendar while waiting on datastore
        # temp_food = [{'foodname':'Chicken', 'date':datetime(2017,8,1)},
        # {'foodname':'Milk', 'date':datetime(2017,7,28)},
        # {'foodname':'Grapes', 'date':datetime(2017,7,31)}]
        # temp_user = 'Brenna'
        # #will attempt to sort temp items in temp_food by expire date

        food_list.sort(key=lambda item:item.date, reverse=False)
        # temp_variables = {'temp_user':temp_user, 'temp_food':temp_food}
        list_template = env.get_template('calendar.html')
        self.response.write(list_template.render(variables))
        #self.response.write(food_list)

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/newfood', NewFoodHandler),
    ('/calendar', ListofExpirationHandler)
], debug=True)
