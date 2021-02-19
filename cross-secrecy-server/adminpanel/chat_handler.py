import uuid
from datetime import datetime
import tornado.web

try:
    import database
    from chat import Chat, Message
except ImportError:
    import adminpanel.database as database
    from adminpanel.chat import Chat, Message

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        value = self.get_secure_cookie("user")
        return None if value is None else value.decode('utf-8')


class ChatMainHandler(BaseHandler):
    def get(self):
        if not self.get_current_user():
            self.redirect("/login")
            return
        chats = database.chat_get_chats_of_user(self.get_current_user())
        self.render('chat/main.html', chats=chats, user=self.get_current_user())

class ChatHandler(BaseHandler):
    def get(self, slug):
        if not self.get_current_user():
            self.redirect("/login")
            return
        chat_id = str(slug)
        chat = Chat(chat_id, viewer=self.get_current_user())
        if not chat.exists() or not self.get_current_user() in chat.get_participants():
            return self.render("404.html", error='Chat with id {} not found.'.format(chat_id))
        self.render('chat/chat.html', chat=chat)

class ChatLoginHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect("/chat/")
        self.render('chat/login.html')

    def check_credentials(self, user, password):
        return database.chat_authenticate(user,password)

    def post(self):
        name     = self.get_argument("name")
        password = self.get_argument("password")
        if self.check_credentials(name, password):
            self.set_secure_cookie("user", name)
            self.redirect("/chat/")
        else:
            self.redirect("/login")

class ChatLogoutHandler(BaseHandler):
    def get(self):
        if not self.get_current_user():
            self.redirect("/login")
        else:
            self.render('chat/logout.html')

    def post(self):
        self.clear_cookie("user")
        self.redirect("/login")


class ChatPostHandler(BaseHandler):

    def post(self):
        chat_id=self.get_argument('chat')
        user=self.get_current_user()
        if not database.chat_exists(chat_id) or not database.chat_user_in_chat(chat_id, user):
            return
        database.chat_add_message(chat_id=chat_id, user=user, date=datetime.now(), text=self.get_argument('message'))
        self.redirect("/chats/{}".format(chat_id))

class ChatCreateHandler(BaseHandler):

    def post(self):
        try:
            # add a user to the existing chat
            chat_id = self.get_argument('chat')
            participant_a = self.get_current_user()
            participant_b = self.get_argument('user')
            if database.chat_exists(chat_id):
                if not database.chat_user_in_chat(chat_id, participant_a):
                    # chat exists and user is not authenticated to add new users
                    return
            else:
                chat_id = database.chat_add_chat(self.get_current_user())
            if not database.chat_user_in_chat(chat_id, participant_b):
                database.chat_add_participant(chat_id, participant_b, check=True)
            self.redirect("/chats/{}".format(chat_id))
        except tornado.web.MissingArgumentError:
            # create a new chat
            new = self.get_argument('new-chat')
            if new:
                chat_id = database.chat_add_chat(self.get_current_user())
            self.redirect("/chats/{}".format(chat_id))
        return
