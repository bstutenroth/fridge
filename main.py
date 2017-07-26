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
            print user.nickname()
            # checks if current user is already in datastore
            checking_var = False
            all_users_query = User.query()
            all_users = all_users_query.fetch()
            for get_user in all_users:
                if user.nickname() == get_user.email:
                    checking_var = True
            # if current user isn't in datatstore, adds them to datastore
            if checking_var == False:
                new_user = User(email=user.nickname())
                new_user.put()
            all_users = User.query().fetch()
            print all_users
        else:
            greeting = ('<div class = "login" ><a href="%s">Sign in or register</a></div>' %
                users.create_login_url('/'))
            all_users = User.query().fetch()
            print all_users
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
            'date':self.request.get('expiredate')
        }
        # stores new food item into datastore and associate them with current user
        user = str(users.get_current_user())
        all_users = User.query().fetch()
        for usernames in all_users:
            print usernames
            if user == usernames.email:
                print usernames.email
                current_user_key = usernames.key
                print current_user_key
                add_food = Food(user_key=current_user_key, foodname= submitted_variables['foodname'], date=datetime.strptime(submitted_variables['date'], '%Y-%m-%d')).put()
                break
        self.redirect("/calendar")

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

        # will use these two lines with datastore
        # brenna=User(name='brenna')
        # brenna_key=brenna.put()
        food_list = Food.query().fetch()
        print food_list
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
