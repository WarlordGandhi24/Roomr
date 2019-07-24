import os

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.api import urlfetch


import json
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def root_parent():
    return ndb.Key('Parent', 'default_parent')

def GetUserChat(user):
    '''Queries datastore to get the current value of the chat associated with this user id.'''
    chats = Chats.query(Chats.from_id == user.user_id(), ancestor=root_parent()).fetch()
    if len(chats) > 0:
        # We found a note, return it.
        return chats[0]
    else:
        # We didn't find a note, return None
        return None
class Chats(ndb.Model):
    from_id = ndb.StringProperty()
    to_id = ndb.StringProperty()
    combo_id = ndb.StringProperty()
    msg = ndb.StringProperty()
class User(ndb.Model):
    '''A database entry representing a single user.'''
    pfpurl = ndb.StringProperty()
    id = ndb.StringProperty()
    name = ndb.StringProperty()
    gender = ndb.StringProperty()
    school = ndb.StringProperty()
    major = ndb.StringProperty()
    public = ndb.StringProperty()
    about_me = ndb.StringProperty()
    noise_level = ndb.StringProperty()
    cleanliness = ndb.StringProperty()
    study_in_room = ndb.StringProperty()
    sleep_time = ndb.StringProperty()
    wake_time = ndb.StringProperty()
    music_genre = ndb.StringProperty()
    movies = ndb.StringProperty()
    misc = ndb.StringProperty()
    user_games = ndb.StringProperty()
    hobbies = ndb.StringProperty()
    firsttime = ndb.StringProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/main.html')
        User.firsttime = True
        User.pfpurl = "http://www.stleos.uq.edu.au/wp-content/uploads/2016/08/image-placeholder-350x350.png"
        login = users.create_login_url('/profile_edit')
        if(User.firsttime == True):
            login = users.create_login_url('/profile_edit')
            User.firsttime = False
        elif(User.firsttime == False):
            login = users.create_login_url('/search')


        data = {
          'user': user,
          'login_url': login,
          'logout_url': users.create_logout_url(self.request.uri),
        }

        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))


class ProfileEditPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user != None:
            template = JINJA_ENVIRONMENT.get_template('templates/profile_edit.html')

            current_user = User.query(User.id == user.user_id()).fetch()
            if(len(current_user) > 0):
                current_user = current_user[0]
            else:
                current_user = User(parent=root_parent())
            print(current_user.about_me)
            self.response.write(template.render({'user' : current_user}))
        else:
            self.redirect('/')
    def post(self):
        print("hi")
        print(self.request.get('user_wake_time'))
        user = users.get_current_user()

        new_user = User.query(User.id == user.user_id(), ancestor=root_parent()).fetch()
        if(len(new_user) > 0):
            new_user = new_user[0]
        else:
            new_user = User(parent=root_parent())
        new_user.id = user.user_id()
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
        new_user.public = self.request.get("user_public")
        new_user.movies = self.request.get("user_movies")
        new_user.games = self.request.get("user_games")
        new_user.misc = self.request.get("user_misc")
        new_user.study_in_room = self.request.get("study_in_room")

        new_user.put()
        self.redirect('/search')

class ProfileViewPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/profile_view.html')
        profId = self.request.get('prof')
        data = []
        for items in User.query(ancestor=root_parent()).fetch():
            if (profId == items.id):
                data = items
        actualData = {
            'user': data
        }
        self.response.write(template.render(actualData))

class SearchPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/search.html')
        toDisplay = User.query(ancestor=root_parent()).fetch()
        data = {
            'users': toDisplay
        }
        self.response.write(template.render(data))

class SearchFilter(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/search.html')
        items = None
        noise = self.request.get("noise")
        print(noise)
        clean = self.request.get("clean")
        print(clean)
        sleep = self.request.get("sleep")
        print(sleep)
        wake = self.request.get("wake")
        print(wake)
        study = self.request.get("study")
        print(study)
        items = User.query()
        if (noise != "Indifferent"):
            items = items.filter(User.noise_level == noise)
        if (clean != "Indifferent"):
            items = items.filter(User.cleanliness == clean)
        if (sleep != "Indifferent"):
            items = items.filter(User.sleep_time == sleep)
        if (wake != "Indifferent"):
            items = items.filter(User.wake_time == wake)
        if (study != "Indifferent"):
            items = items.filter(User.study_in_room == study)
        items = items.fetch()
         # and (User.cleanliness == clean) and (User.sleep_time == sleep) and (User.wake_time == wake) and (User.study_in_room == study)).fetch()
        #print(items)
        #queryItem = User.query((User.cleanliness == clean) and (User.sleep_time == sleep) and (User.wake_time == wake) and (User.study_in_room == study))
        data = {
            'users': items
        }
        self.response.write(template.render(data))

class AjaxProfilePictureSave(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        new_user = User.query(User.id == user.user_id(), ancestor=root_parent()).fetch()
        new_user.pfpurl = json.loads(self.request.body)["answer"]
        #data = {'url': note}
        #User.pfpurl = self.request.get("answer")


class ChatPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/chat.html')

        chats = Chats.query(Chats.from_id == user.user_id(), ancestor=root_parent()).fetch()

        data ={
        'chats': chats,
        'initialCount' : len(chats)
        }
        self.response.write(template.render(data))
    def post(self):
        user = users.get_current_user()
        newChat = Chats(parent=root_parent())
        newChat.from_id = user.user_id()
        newMsg = self.request.get("userMsg")
        newChat.msg = newMsg
        newChat.put()
        self.redirect("/chat")

class AjaxGetNewMsg(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            # No user is logged in, so don't return any value.
            self.response.status = 401
            return
        chat = GetUserChat(user)
        msg = ''
        if chat is not None:
            # If there was a current note, update note.
            msg = chat.msg

        # build a dictionary that contains the data that we want to return.
        chatFromUser = Chats.query(Chats.from_id == user.user_id(),ancestor=root_parent()).fetch()
        print(chatFromUser)
        msgs = []
        for x in chatFromUser:
            msgs.append(x.msg)
        data = {
        'msgCount': len(chatFromUser),
        'msgs': msgs
        }
        # Note the different content type.
        self.response.headers['Content-Type'] = 'application/json'
        # Turn data dict into a json string and write it to the response
        self.response.write(json.dumps(data))



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/profile_edit', ProfileEditPage),
    ('/profile_view', ProfileViewPage),
    ('/search', SearchPage),
    ('/searchfilter', SearchFilter),
    ('/ajax/get_updated_log', AjaxGetNewMsg),
    ('/chat', ChatPage),
    ('/ajax/update_pfp', AjaxProfilePictureSave)
], debug=True)
