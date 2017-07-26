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
        self.redirect("/")

#Displaying on Calendar Handler
class ListofExpirationHandler(webapp2.RequestHandler):
    def get (self):
        current_user_food = []
        user = str(users.get_current_user())
        all_users = User.query().fetch()
        food_list = Food.query().fetch()
        for usernames in all_users:
            if user == usernames.email:
                current_user_key = usernames.key
        for fooditems in food_list:
            if current_user_key == fooditems.user_key:
                current_user_food.append(fooditems)
        current_user_food.sort(key=lambda item:item.date, reverse=False)
        variables = {'username':user,'food_list':current_user_food}
        list_template = env.get_template('calendar.html')
        self.response.write(list_template.render(variables))

    def post(self):
        idtodelete=self.request.get("deletelist")
        print idtodelete
        foodtodelete=Food.query(Food.foodname == idtodelete).get()
        print foodtodelete
        foodtodelete.key.delete()
        self.redirect('/')



app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/newfood', NewFoodHandler),
    ('/calendar', ListofExpirationHandler)
], debug=True)
