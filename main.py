import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from food import User
from food import Food
import datetime

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class HomeHandler(webapp2.RequestHandler):
    def get (self):
        print('hi')
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
            'month':str(self.request.get("month")),
            'year':str(self.request.get("year")),
            'day':str(self.request.get("day"))
        }
        brenna=User(name='brenna')
        brenna_key=brenna.put()
        food1 = Food(user_key=brenna_key, foodname= submitted_variables['foodname'], month=int(submitted_variables['month']),year=int(submitted_variables['year']),day=int(submitted_variables['day']))
        food1_key=food1.put()
# don't think we need these next 4 lines, but didn't want to totally delete
# before checking up with everyone
#        food_list = Food.query().fetch()
#        variables = {'food_list': food_list}
#        list_template = env.get_template('calendar.html')
#        self.response.write(list_template.render(variables))

#Displaying on Calendar Handler
class ListofExpirationHandler(webapp2.RequestHandler):
    def get (self):
        #will use these two lines with datastore
        food_list = Food.query().fetch()
        variables = {'food_list': food_list}

        #temp variable list to display on calendar while waiting on datastore
        temp_food = [{'foodname':'Chicken', 'category':'Meat', 'expire_date':datetime.date(2017,8,1)},
        {'foodname':'Milk', 'category':'Dairy', 'expire_date':datetime.date(2017,7,31)},
        {'foodname':'Grapes', 'category':'Fruit', 'expire_date':datetime.date(2017,7,28)}]
        temp_user = 'Brenna'
        temp_variables = {'temp_user':temp_user, 'temp_food':temp_food}

        #will attempt to sort temp items in temp_food by expire date

        list_template = env.get_template('calendar.html')
        self.response.write(list_template.render(temp_variables))

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/newfood', NewFoodHandler),
    ('/calendar', ListofExpirationHandler)
], debug=True)
