import webapp2
import jinja2
import os
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get (self):
        template = env.get_template('newfood.html')
        newfood_variables = {
            'name':self.request.get("name"),
            'category':self.request.get("category"),
            'expire_date':self.request.get("expire_date"),
        }
        self.response.out.write(template.render(newfood_variables))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
