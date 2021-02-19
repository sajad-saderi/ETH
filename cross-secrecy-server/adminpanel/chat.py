import uuid
from datetime import datetime

try:
    import database
except ImportError:
    import adminpanel.database as database

class Chat():
    def __init__(self, id:str=None, viewer:str=None):
        self.id          = id
        self.viewer      = viewer

    def add_participant(self, user:str):
        database.chat_add_participant(self.id, user)

    def get_participants(self):
        return database.chat_get_participants(self.id)

    def get_messages(self):
        messages = database.chat_get_messages(self.id)
        for message in messages:
            message.viewer=self.viewer
        return messages

    def exists(self):
        return database.chat_exists(self.id)

class Message():
    def __init__(self, chat_id, user, text, id=None, date=None, viewer:str=None):
        self.chat_id     = chat_id
        self.id          = id
        self.date        = date
        self.user        = user
        self.text        = text
        self.viewer      = viewer

        if id is None:
            database.chat_add_message(self.chat_id, self.user, datetime.now() if date is None else date, self.text)

    def is_from_viewer(self):
        return self.user == self.viewer
