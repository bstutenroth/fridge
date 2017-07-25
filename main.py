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
        submit_template = env.get_template('submit.html')
        submitted_variables = {
            'foodname':self.request.get("foodname"),
            'category':self.request.get("category"),
            'expire_date':self.request.get("expire_date")
        }
        self.response.out.write(submit_template.render(submitted_variables))

class ListofExpirationHandler(webapp2.RequestHandler):
    def get (self):
        brenna=User(name='brenna')
        brenna_key=brenna.put()
        food1 = Food(user_key=brenna_key, foodname= 'beef', expire_date=datetime.datetime(2017, 7, 29))
        food1_key=food1.put()
        variables = {'food1': food1}
        food_list = food1.query().fetch()
        list_template = env.get_template('calendar.html')
        self.response.write(list_template.render(variables))

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/newfood', NewFoodHandler),
    ('/calendar', ListofExpirationHandler)
], debug=True)
