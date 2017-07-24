import webapp2
import jinja2
import os

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class HomeHandler(webapp2.RequestHandler):
    def get (self):
        template = env.get_template('homepage.html')
        self.response.out.write(template.render())

class NewFoodHandler(webapp2.RequestHandler):
    def get (self):
        newfood_template = env.get_template('newfood.html')
        newfood_variables = {
            'name':self.request.get("name"),
            'category':self.request.get("category"),
            'expire_date':self.request.get("expire_date"),
        }
        self.response.out.write(newfood_template.render(newfood_variables))

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/newfood', NewFoodHandler)
], debug=True)
