import webapp2
import jinja2
import os
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/submit.html')
        self.response.write(template.render())
    def post (self):
        results_template = env.get_template('results.html')
        template_variables = {
            'name':self.request.get("name"),
            'category':self.request.get("category"),
            'expire_date':self.request.get("expire_date"),
        }
        self.response.out.write(results_template.render(template_variables))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
