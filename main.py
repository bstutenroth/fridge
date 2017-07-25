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

    def post(self):
        submitted_variables = {
            'foodname':self.request.get("foodname"),
            'category':self.request.get("category"),
            'month':self.request.get("month")
            'year':self.request.get("year")
            'day':self.request.get("day")
        }
        brenna=User(name='brenna')
        brenna_key=brenna.put()
        food1 = Food(user_key=brenna_key, foodname= submitted_variables.foodname, month=submitted_variables.month,year=submitted_variables.year,day=submitted_variables.day)
        food1_key=food1.put()
        food_list = Food.query().fetch()
        variables = {'food_list': food_list}
        list_template = env.get_template('calendar.html')
        self.response.write(list_template.render(variables))

class ListofExpirationHandler(webapp2.RequestHandler):
    def get (self):

        food_list = Food.query().fetch()
        variables = {'food_list': food_list}
        list_template = env.get_template('calendar.html')
        self.response.write(list_template.render(variables))

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/newfood', NewFoodHandler),
    ('/calendar', ListofExpirationHandler)
], debug=True)
