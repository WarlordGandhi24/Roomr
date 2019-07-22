import os

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import images


import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def root_parent():
    return ndb.Key('Parent', 'default_parent')

class User(ndb.Model):
    '''A database entry representing a single user.'''
    pfp = ndb.BlobProperty()
    name = ndb.StringProperty()
    gender = ndb.StringProperty()
    school = ndb.StringProperty()
    major = ndb.StringProperty()
    about_me = ndb.StringProperty()
    noise_level = ndb.StringProperty()
    cleanliness = ndb.StringProperty()
    study_in_room = ndb.BooleanProperty()
    sleep_time = ndb.StringProperty()
    wake_time = ndb.StringProperty()
    music_genre = ndb.StringProperty()
    hobbies = ndb.StringProperty()





class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/main.html')
        data = {
          'user': user,
          'login_url': users.create_login_url(self.request.uri),
          'logout_url': users.create_logout_url(self.request.uri),
        }

        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))
    def post(self):
        new_user = User(parent=root_parent())

        new_user.name = self.request.get('user_name')
        new_user.gender = self.request.get('user_gender')
        new_user.school = self.request.get('user_school')
        new_user.major = self.request.get('user_major')
        new_user.about_me = self.request.get('user_about_me')
        new_user.noise_level = self.request.get('user_noise_level')
        new_user.cleanliness = self.request.get('user_cleanliness')
        new_user.sleep_time = self.request.get('user_sleep_time')
        new_user.wake_time = self.request.get('user_wake_time')
        new_user.music_genre = self.request.get('user_music_genre')
        new_user.hobbies = self.request.get('user_hobbies')
        new_user.study_in_room = bool(self.request.get('user_study_in_room', default_value=''))
        new_user.put()

class ProfileEditPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/profile_edit.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())

class ProfileViewPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/profile_view.html')
        self.response.write(template.render())

class SearchPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/search.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/profile_edit', ProfileEditPage),
    ('/profile_view', ProfileViewPage),
    ('/search', SearchPage)
], debug=True)
