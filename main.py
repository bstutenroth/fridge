import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail
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
            # checks if current user is already in datastore
            checking_var = False
            all_users_query = User.query(User.email==user.nickname())
            person = all_users_query.get()

            # we didn't get any matching users
            if not person:
                print 'a'
            # we found 'em
            else:
                checking_var = True
                variables = {'username':person.email}
                print 'b'

        #     all_users = all_users_query.fetch()
        #    for get_user in all_users:
        #         if user.nickname() == get_user.email:
        #             checking_var = True
        #             current_user_list = get_user


            # if current user isn't in datatstore, adds them to datastore
            if checking_var == False:
                new_user = User(email=user.nickname(),consume=0, expire=0)
                new_user.put()

                variables = {'username':new_user}
        #    all_users = User.query().fetch()
        else:
            greeting = ('<div class = "login" ><a href="%s">Sign in or register</a></div>' %
                users.create_login_url('/'))
            variables = {'username':""}
    #        all_users = User.query().fetch()
        self.response.write('<html><body>%s</body></html>' % greeting)
        template = env.get_template('homepage.html')
        self.response.out.write(template.render(variables))

class NewFoodHandler(webapp2.RequestHandler):
    def get (self):
        user = users.get_current_user()
        if user == None:
            greeting = ('<div id = "other_login" ><a href="%s">Sign in or register</a></div>' %
                            users.create_login_url('/'))
            self.response.write('<html><body>%s</body></html>' % greeting)
            login_template = env.get_template('Login.html')
            self.response.out.write(login_template.render())
        else:
            variables = {'username':user}
            newfood_template = env.get_template('newfood.html')
            self.response.out.write(newfood_template.render(variables))

#Adding New Food to Datastore
    def post(self):
        user = users.get_current_user()
        submitted_variables = {
            'foodname':self.request.get("foodname"),
            'date':self.request.get('expiredate'),
            'category':self.request.get('button')
        }
        # stores new food item into datastore and associate them with current user
        # user = str(users.get_current_user())
        # all_users = User.query().fetch()
        # for usernames in all_users:
        #     print usernames
        #     if user == usernames.email:
        #         print usernames.email
        #         current_user_key = usernames.key
        #         print current_user_key
        add_food = Food(user_email=user.nickname(), foodname= submitted_variables['foodname'], date=datetime.strptime(submitted_variables['date'], '%Y-%m-%d'), category=submitted_variables['category']).put()
        self.redirect("/")

#Displaying on Calendar Handler
class ListofExpirationHandler(webapp2.RequestHandler):
    def get (self):
        user = users.get_current_user()
        all_users = User.query(User.email==user.nickname()).get()
        if user == None:
            greeting = ('<div id = "other_login" ><a href="%s">Sign in or register</a></div>' %
                            users.create_login_url('/'))
            self.response.write('<html><body>%s</body></html>' % greeting)
            login_template = env.get_template('Login.html')
            self.response.out.write(login_template.render())
        else:
            current_user_food = []
            user = users.get_current_user()
            food_list = Food.query().fetch()
            for fooditems in food_list:
                if user.nickname() == fooditems.user_email:
                    current_user_food.append(fooditems)
            current_user_food.sort(key=lambda item:item.date, reverse=False)
            variables = {'username':user.nickname(),'food_list':current_user_food, 'count':all_users}
            list_template = env.get_template('calendar.html')
            self.response.write(list_template.render(variables))

    def post(self):
        idtodelete=self.request.get("deletelist")
        deletetype=self.request.get('deletetype')
        all_users = User.query().fetch()
        food_list = Food.query().fetch()
        if deletetype == 'consume':
            current_user = str(users.get_current_user())
            for usernames in all_users:
                if current_user == usernames.email:
                    usernames.consume += 1
                    usernames.put()
        elif deletetype == 'expire':
            current_user = str(users.get_current_user())
            for usernames in all_users:
                if current_user == usernames.email:
                    usernames.expire += 1
                    usernames.put()
        foodtodelete=Food.query(Food.foodname == idtodelete).get()
        foodtodelete.key.delete()
        self.redirect('/')

class FridgeHandler(webapp2.RequestHandler):
    def get (self):
        user = users.get_current_user()
        all_users = User.query(User.email==user.nickname()).get()
        if user == None:
            greeting = ('<div id = "other_login" ><a href="%s">Sign in or register</a></div>' %
                            users.create_login_url('/'))
            self.response.write('<html><body>%s</body></html>' % greeting)
            login_template = env.get_template('Login.html')
            self.response.out.write(login_template.render())
        else:
            current_user_food = []
            food_list = Food.query().fetch()
            for fooditems in food_list:
                if user.nickname() == fooditems.user_email:
                    current_user_food.append(fooditems)
            print current_user_food
            variables = {'username':user.nickname(),'food_list':current_user_food, 'count':all_users}
            list_template = env.get_template('myfridge.html')
            self.response.write(list_template.render(variables))

    def post(self):
        idtodelete=self.request.get("deletelist")
        deletetype=self.request.get('deletetype')
        all_users = User.query().fetch()
        food_list = Food.query().fetch()
        if deletetype == 'consume':
            current_user = str(users.get_current_user())
            for usernames in all_users:
                if current_user == usernames.email:
                    usernames.consume += 1
                    usernames.put()
        elif deletetype == 'expire':
            current_user = str(users.get_current_user())
            for usernames in all_users:
                if current_user == usernames.email:
                    usernames.expire += 1
                    usernames.put()
        foodtodelete=Food.query(Food.foodname == idtodelete).get()
        foodtodelete.key.delete()
        self.redirect('/')

# def send_approved_mail(sender_address):
#     message = mail.EmailMessage(sender="<brennastutenroth@gmail.com>",
#         to="Brenna <brennastutenroth@gmail.com>",
#         subject="My Fridge Daily Reminder",
#         body="""Dear User:
#         This is your daily reminder to check your items' expiration dates at
#         http://my-fridge-174900.appspot.com
#         - The My Fridge App Team""")
#
# class SendMailHandler(webapp2.RequestHandler):
#     def get(self):
#         send_approved_mail('{}@appspot.gserviceaccount.com'.format(
#             app_identity.get_application_id()))
#         self.response.content_type = 'text/plain'
#         self.response.write('Sent test email.')
def send_approved_mail(sender_address):
    # [START send_message]
    message = mail.EmailMessage(
        sender=sender_address,
        subject="Your account has been approved")

    message.to = "Albert Johnson <brennastutenroth@gmail.com>"
    message.body = """Dear User:
his is your daily reminder to check your items' expiration dates at
http://my-fridge-174900.appspot.com
- The My Fridge App Team
"""
    message.send()
    # [END send_message]


class SendMessageHandler(webapp2.RequestHandler):
    def get(self):
        send_approved_mail('{}@appspot.gserviceaccount.com'.format(
            app_identity.get_application_id()))
        self.response.content_type = 'text/plain'
        self.response.write('Sent an email reminder')


app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/newfood', NewFoodHandler),
    ('/calendar', ListofExpirationHandler),
    ('/myfridge', FridgeHandler),
    # ('/send_mail', SendMailHandler)
    ('/send_message', SendMessageHandler),
], debug=True)
