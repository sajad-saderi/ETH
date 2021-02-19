import sqlite3
import logging
from tornado import options

try:
    from issue import Issue
    from chat import Chat, Message
except ImportError:
    from adminpanel.issue import Issue
    from adminpanel.chat import Chat, Message

issue_conn = None
chat_conn = None
path = None

def close():
    global issue_conn
    issue_conn.commit()
    issue_conn.close()

def setup(path_: str):
    global issue_conn
    global chat_conn
    global path
    path = path_
    issue_conn = sqlite3.connect(path_)
    chat_conn = sqlite3.connect(path_)
    conn = sqlite3.connect(path_)
    logging.info('Creating Tables')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS "issues" (
	"id"	INTEGER UNIQUE,
	"date"	TEXT,
	"author"	TEXT,
	"subject"	TEXT,
	"description"	TEXT,
	"image"	TEXT,
	PRIMARY KEY("id")
);""")
    c.execute("""CREATE TABLE IF NOT EXISTS "users" (
	"name"	TEXT UNIQUE,
	"password"	TEXT,
	PRIMARY KEY("name")
);""")
    c.execute("""CREATE TABLE IF NOT EXISTS "chats" (
	"id"	INTEGER,
	"name"	TEXT
);""")
    c.execute("""CREATE TABLE IF NOT EXISTS "messages" (
	"id"	  INTEGER UNIQUE,
	"chat_id"	INTEGER,
	"name"	TEXT,
	"date"	TEXT,
	"message"	TEXT,
	PRIMARY KEY("id")
);""")
    c.execute("""INSERT OR IGNORE INTO users (name, password) VALUES ("admin", "8739e041239b27d6b44a5db05cd1ed41");""")
    c.execute("""INSERT OR IGNORE INTO users (name, password) VALUES ("robert_jackson", "crosssecrecy123");""")
    c.execute("""INSERT OR IGNORE INTO users (name, password) VALUES ("barbara_dean", "pa55word");""")
#    c.execute("""INSERT OR IGNORE INTO users (name, password) VALUES ("joellen_oyler", "ghklasdf");""")
#    c.execute("""INSERT OR IGNORE INTO chats (id, name) VALUES ("1","robert_jackson");""")
#    c.execute("""INSERT OR IGNORE INTO chats (id, name) VALUES ("1","barbara_dean");""")
#    c.execute("""INSERT INTO messages (chat_id, name, date, message) VALUES ("1","robert_jackson","2020-11-17 18:15:20.452314","Hello!");""")
    conn.commit()

def add_issue(issue: Issue, threading = False):
    if threading:
        conn_ = sqlite3.connect(path)
    else:
        conn_ = issue_conn
    c = conn_.cursor()
    c.execute('INSERT INTO issues (id, date, author, subject, description, image) VALUES (?,?,?,?,?,?);', (issue.id, issue.date,issue.author,issue.subject,issue.description,issue.image))
    conn_.commit()
    if threading:
        conn_.close()

def remove_issue(issue_id: int, threading = False):
    if threading:
        conn_ = sqlite3.connect(path)
    else:
        conn_ = issue_conn
    c = conn_.cursor()
    c.execute('DELETE FROM issues WHERE id=:id;', {'id': issue_id})
    conn_.commit()
    if threading:
        conn_.close()


def get_next_id(threading = False):
    if threading:
        conn_ = sqlite3.connect(path)
    else:
        conn_ = issue_conn
    c = conn_.cursor()
    try:
        next_id = int(c.execute('SELECT max(id) FROM issues;').fetchone()[0]) + 1
    except TypeError:
        next_id = 1
    if threading:
        conn_.close()
    return next_id

def get_issue(id_:int=-1):
    c = issue_conn.cursor()
    r = c.execute('SELECT author, subject, description, image, id, date FROM issues WHERE id=:id;', {'id': id_}).fetchone() if id_>-1 \
        else c.execute('SELECT author, subject, description, image, id, date FROM issues ORDER BY(id) DESC LIMIT 30').fetchall()
    if id_>-1:
        if r is None:
            return None
        return Issue(r[0],r[1],r[2],r[3],id=r[4],date=r[5])
    else:
        return [Issue(r_[0],r_[1],r_[2],r_[3],id=r_[4],date=r_[5]) for r_ in r]

def commit_issue(issue):
    c = issue_conn.cursor()
    c.execute( '''INSERT INTO issues(id, date, author, subject, description, image) VALUES(?,?,?,?,?,?);''', (issue.id, issue.date, issue.author, issue.subject, issue.description, issue.image))
    issue_conn.commit()



def chat_authenticate(user,password):
    c = chat_conn.cursor()
    r = c.execute('SELECT name FROM users WHERE name=:name AND password=:password;', {'name': user, 'password': password}).fetchone()
    return r is not None

def chat_add_message(chat_id, user, date, text, threading = False):
    if threading:
        conn_ = sqlite3.connect(path)
    else:
        conn_ = chat_conn
    c = conn_.cursor()
    c.execute('INSERT INTO messages (chat_id, name, date, message) VALUES (?,?,?,?);', (chat_id, user, date, text))
    conn_.commit()
    if threading:
        conn_.close()

def chat_get_messages(chat_id):
    c = chat_conn.cursor()
    r = c.execute('SELECT id, name, message, date FROM messages WHERE chat_id=:chat_id;', {'chat_id': chat_id})
    return [Message(chat_id, r_[1], r_[2], id=r_[0], date=r_[3]) for r_ in r]


def chat_get_participants(chat_id):
    c = chat_conn.cursor()
    r = c.execute('SELECT name FROM chats WHERE id=:chat_id;', {'chat_id': chat_id})
    return [r_[0] for r_ in r]

def chat_get_chats_of_user(user):
    c = chat_conn.cursor()
    r = c.execute('SELECT id FROM chats WHERE name=:user;', {'user': user})
    return [Chat(id=r_[0], viewer=user) for r_ in r]

def chat_add_participant(chat_id, user, check=True, threading = False):
    if threading:
        conn_ = sqlite3.connect(path)
    else:
        conn_ = chat_conn
    c = conn_.cursor()
    if check:
        r = c.execute('SELECT name FROM users WHERE name=:name;', {'name': user}).fetchone()
        if not r:
            if threading:
                conn_.close()
            return

    c.execute('INSERT INTO chats (id, name) VALUES (?,?);', (chat_id, user))
    conn_.commit()
    if threading:
        conn_.close()



def chat_exists(chat_id):
    c = chat_conn.cursor()
    r = c.execute('SELECT id FROM chats WHERE id=:id;', {'id': chat_id}).fetchone()
    return r is not None

def chat_user_in_chat(chat_id, user):
    c = chat_conn.cursor()
    r = c.execute('SELECT id FROM chats WHERE id=:id AND name=:user;', {'id': chat_id, 'user': user}).fetchone()
    return r is not None


def chat_get_next_id(threading = False):
    if threading:
        conn_ = sqlite3.connect(path)
    else:
        conn_ = chat_conn
    c = conn_.cursor()
    try:
        next_id = int(c.execute('SELECT max(id) FROM chats;').fetchone()[0]) + 1
    except TypeError:
        next_id = 1
    if threading:
        conn_.close()
    return next_id

def chat_add_chat(user, threading = False):
    next_id = chat_get_next_id()
    if threading:
        conn_ = sqlite3.connect(path)
    else:
        conn_ = chat_conn
    c = conn_.cursor()
    c.execute('INSERT INTO chats (id, name) VALUES (?,?);', (next_id, user))
    conn_.commit()
    if threading:
        conn_.close()

    return next_id
