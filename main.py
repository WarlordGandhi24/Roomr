import os

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.api import urlfetch
from google.appengine.ext import db

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

class Chatrooms(ndb.Model):
    from_id = ndb.StringProperty()
    to_id = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
class Messages(ndb.Model):
    chatKey = ndb.StringProperty()
    sentId = ndb.StringProperty()
    msg = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
class User(ndb.Model):
    '''A database entry representing a single user.'''
    pfpurl = ndb.StringProperty()
    id = ndb.StringProperty()
    name = ndb.StringProperty()
    gender = ndb.StringProperty()
    school = ndb.StringProperty()
    major = ndb.StringProperty()
    private = ndb.StringProperty()
    about_me = ndb.StringProperty()
    noise_level = ndb.StringProperty()
    cleanliness = ndb.StringProperty()
    study_in_room = ndb.StringProperty()
    sleep_time = ndb.StringProperty()
    wake_time = ndb.StringProperty()
    music_genre = ndb.StringProperty()
    movies = ndb.StringProperty()
    misc = ndb.StringProperty()
    games = ndb.StringProperty()
    hobbies = ndb.StringProperty()
    firsttime = ndb.StringProperty()
    roomies = ndb.StringProperty(repeated = True)
class ChatRemember(ndb.Model):
    name = ndb.StringProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/main.html')
        User.firsttime = True
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

def getList():
    list = 'http://universities.hipolabs.com/search?country=United%20States'
    list_resp = urlfetch.Fetch(list).content
    return json.loads(list_resp)

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
            list = getList()
            data = {
                'user': current_user,
                'colleges': list,
            }
            self.response.write(template.render(data))
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
        new_user.private = self.request.get("private")
        new_user.movies = self.request.get("user_movies")
        new_user.games = self.request.get("user_games")
        new_user.misc = self.request.get("user_misc")
        new_user.study_in_room = self.request.get("study_in_room")
        new_user.roomies = []
        new_user.put()
        self.redirect('/search')

class ProfileViewPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/profile_view.html')
        current_user = User.query(User.id == user.user_id(), ancestor=root_parent()).fetch()
        profId = self.request.get('prof')
        isRoomie = False
        if profId in current_user[0].roomies:
            isRoomie = True
        data = []
        for items in User.query(ancestor=root_parent()).fetch():
            if (profId == items.id):
                data = items
                print("???????????????????????????")
                print(items.pfpurl)
        actualData = {
            'user': data,
            'isRoomie': isRoomie
        }
        self.response.write(template.render(actualData))

class SearchPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        current_user = User.query(User.id == user.user_id(), ancestor=root_parent()).fetch()
        template = JINJA_ENVIRONMENT.get_template('templates/search.html')
        toDisplay = User.query(User.private == "Public", ancestor=root_parent()).fetch()
        friends = []
        for x in current_user[0].roomies:
            userToGet = User.query(User.id == x, ancestor=root_parent()).fetch()
            friends.extend(userToGet)
            print(userToGet)
        data = {
            'users': toDisplay,
            'userId': user.user_id(),
            'roomies': friends
        }
        print("!!!!!!!!!!2i3401i90312849124891274812487123")
        print(friends)
        self.response.write(template.render(data))


    def post(self):
        otherId = self.request.get("otherId")
        print(otherId)
        user = users.get_current_user()
        chatroom = Chatrooms.query(ndb.OR(
        ndb.AND(Chatrooms.from_id == otherId, Chatrooms.to_id == user.user_id()),
        ndb.AND(Chatrooms.to_id == otherId, Chatrooms.from_id == user.user_id())
        ), ancestor=root_parent()).fetch()
        print(chatroom)
        if(len(chatroom) == 0):
            chatroom = Chatrooms(parent=root_parent())
            chatroom.from_id = user.user_id()
            chatroom.to_id = otherId
            chatroom.put()
            self.redirect("/chat?otherId=" + otherId + "otherUser?=")
        else:
            self.redirect("/chat?otherId=" + otherId)




class SearchFilter(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/search.html')
        user = users.get_current_user()
        current_user = User.query(User.id == user.user_id(), ancestor=root_parent()).fetch()
        noise = self.request.get("noise")
        clean = self.request.get("clean")
        sleep = self.request.get("sleep")
        wake = self.request.get("wake")
        study = self.request.get("study")
        gender = self.request.get("gender")
        if (noise == "Select"):
            noise = "Indifferent"
        if (clean == "Select"):
            clean = "Indifferent"
        if (sleep == "Select"):
            sleep = "Indifferent"
        if (wake == "Select"):
            wake = "Indifferent"
        if (study == "Select"):
            study = "Indifferent"
        if (gender == "Select"):
            gender = "Indifferent"
        items = User.query()
        items = items.filter(User.school == current_user[0].school)
        items = items.filter(User.private == "Public")
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
        if (gender != "Indifferent"):
            items = items.filter(User.gender == gender)
        items = items.fetch()
         # and (User.cleanliness == clean) and (User.sleep_time == sleep) and (User.wake_time == wake) and (User.study_in_room == study)).fetch()
        #print(items)
        #queryItem = User.query((User.cleanliness == clean) and (User.sleep_time == sleep) and (User.wake_time == wake) and (User.study_in_room == study))
        data = {
            'users': items
        }
        self.response.write(template.render(data))

class AddRoomies(webapp2.RequestHandler):
    def post(self):
        roomieToAdd = self.request.get("roomieToAdd")
        roomieToAdd = str(roomieToAdd)
        user = users.get_current_user()
        print(roomieToAdd)
        current_user = User.query(User.id == user.user_id(), ancestor=root_parent()).fetch()
        current_user[0].roomies.append(roomieToAdd)
        current_user[0].put()
        self.redirect("/search")

class KillRoomies(webapp2.RequestHandler):
    def post(self):
        roomieToKill = self.request.get("roomieToKill")
        user = users.get_current_user()
        current_user = User.query(User.id == user.user_id(), ancestor=root_parent()).fetch()
        current_user[0].roomies.remove(roomieToKill)
        current_user[0].put()
        self.redirect("/search")

class AjaxProfilePictureSave(webapp2.RequestHandler):
    def post(self):
        #new_user = User.query(User.id == user.user_id(), ancestor=root_parent()).fetch()
        #data = {'url': note}
        #User.pfpurl = self.request.get("answer")
        user = users.get_current_user()

        new_user = User.query(User.id == user.user_id(), ancestor=root_parent()).fetch()
        if(len(new_user) > 0):
            new_user = new_user[0]
        else:
            new_user = User(parent=root_parent())
            new_user.id = user.user_id()

        new_user.pfpurl = json.loads(self.request.body)["answer"]
        print new_user
        new_user.put()
        print(new_user.pfpurl)


class ChatPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        otherId = self.request.get("otherId")
        otherUser = User.query(User.id == otherId, ancestor=root_parent()).fetch()
        otherUser = otherUser[0]

        print("TEST" + otherId)

        template = JINJA_ENVIRONMENT.get_template('templates/chat.html')
        chatroom = Chatrooms.query(ndb.OR(
        ndb.AND(Chatrooms.from_id == otherId, Chatrooms.to_id == user.user_id()),
        ndb.AND(Chatrooms.to_id == otherId, Chatrooms.from_id == user.user_id())
        ), ancestor=root_parent()).fetch()
        print(len(chatroom))
        chatroom = chatroom[0]

        messages = Messages.query(str(chatroom.key.id()) == Messages.chatKey, ancestor=root_parent()).order(Messages.date).fetch()


        data = {
            'chatKey': chatroom.key.id(),
            'otherId': otherId,
            'otherUser': otherUser,
            'messages': messages,
            'userId': user.user_id(),
            'initialCount' : len(messages),
        }
        self.response.write(template.render(data))
    def post(self):
        user = users.get_current_user()
        newMsg = Messages(parent=root_parent())
        newMsg.chatKey = self.request.get("chatKey")
        otherId = self.request.get("otherId")
        newMsg.msg = self.request.get("userMsg")
        newMsg.sentId = user.user_id()
        newMsg.put()
        self.redirect("/chat?otherId=" + otherId)

class AjaxGetNewMsg(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            # No user is logged in, so don't return any value.
            self.response.status = 401
            return
        otherId = self.request.get("otherId")
        print(otherId)
        chatroom = Chatrooms.query(ndb.OR(
        ndb.AND(Chatrooms.from_id == otherId, Chatrooms.to_id == user.user_id()),
        ndb.AND(Chatrooms.to_id == otherId, Chatrooms.from_id == user.user_id())
        ), ancestor=root_parent()).fetch()
        chatroom = chatroom[0]
        # build a dictionary that contains the data that we want to return.
        messages = Messages.query(str(chatroom.key.id()) == Messages.chatKey, ancestor=root_parent()).order(Messages.date).fetch()
        ids = []
        msgs=[]

        for x in messages:
            msgs.append([x.msg, x.sentId])
        data = {
        'msgCount': len(messages),
        'msgs': msgs,
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
    ('/ajax/update_pfp', AjaxProfilePictureSave),
    ('/roomie', AddRoomies),
    ('/rkill', KillRoomies)
], debug=True)
