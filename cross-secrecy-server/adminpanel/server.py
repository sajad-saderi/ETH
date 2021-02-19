import logging
import argparse
import os.path

import tornado.ioloop
import tornado.web
import tornado.template
import tornado.httpserver
import tornado.escape
from tornado.options import define, options

try:
    from issue_handler import IssueHandler, IssuesHandler, IssuePostHandler, IssueImageHandler, IssueRemoveHandler
    from chat_handler import ChatHandler, ChatMainHandler, ChatLoginHandler, ChatLogoutHandler, ChatPostHandler, ChatCreateHandler
    from escape import cross_secrecy_escape, chat_escape
    from issue_creator import issue_scheduler
    import database
except ImportError:
    from adminpanel.issue_handler import IssueHandler, IssuesHandler, IssuePostHandler, IssueImageHandler, IssueRemoveHandler
    from adminpanel.chat_handler import ChatHandler, ChatMainHandler, ChatLoginHandler, ChatLogoutHandler, ChatPostHandler, ChatCreateHandler
    from adminpanel.escape import cross_secrecy_escape, chat_escape
    from adminpanel.issue_creator import issue_scheduler
    import adminpanel.database as database


define('database', default='./database.sqlite3', help='database path', type=str)
define('data', default='./data', help='path that holds static and template data', type=str)
define('port-issueserver', default=3333, help='issue server port', type=int)
define('port-chatserver', default=8008, help='chatserver port', type=int)
define('port-adminpanel', default=8080, help='adminpanel port', type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")

class IssueModule(tornado.web.UIModule):
    def render(self, issue):
        return self.render_string("modules/issue.html", issue=issue)


def admin_server(data_path, port=8080):
    """
    Prepare the adminpanel web server that allows admins to manage issues.
    Server runs on port 8080.
    """
    handlers = [
        (r"/", MainHandler), # Front page
        (r"/issues/([^/]+)", IssueHandler), # Show a single issue identified by ID
        (r'/issues/', IssuesHandler), # List the latest n issues
        (r"/issues/([^/]+)/close", IssueRemoveHandler), # Show an issue by ID
        (r'/chat/', ChatMainHandler),
        (r'/login', ChatLoginHandler),
        (r'/logout', ChatLogoutHandler),
        (r'/chat/post', ChatPostHandler),
        (r'/chat/add', ChatCreateHandler),
        (r'/chats/([^/]+)', ChatHandler)
    ]
    settings = dict(
        cookie_secret="Q48NUp1dBWRJZYuv0LNo7riGQkaF5e01yijHzngBavYl7KIUZY",
        static_path=os.path.join(data_path, "static"),
        xsrf_cookies=True,
        ui_modules={"Issue": IssueModule},
        debug=True,
        template_loader=tornado.template.Loader(
                os.path.join(data_path, "templates"),
                namespace = {'cross_secrecy_escape': cross_secrecy_escape, 'chat_escape': chat_escape},
                autoescape = 'cross_secrecy_escape', whitespace = 'oneline'
            ),
        title="Cross-Secrecy Admin Panel",
    )
    application = tornado.web.Application(handlers, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port, address='0.0.0.0')

def public_issue_server(port=3333):
    """
    Prepare a server that accepts new issues and inserts those into the databases.
    Server runs on port 3333.
    """
    handlers = [
        (r'/issue', IssuePostHandler),
    ]
    settings = dict(
        cookie_secret="OEHyZ7lXg3C2NQu0vnJkxjCQsOFQeSeyJ1KWIJkgCD1MiwK9rr",
        xsrf_cookies=False,
        debug=True
    )
    application = tornado.web.Application(handlers, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port, address='0.0.0.0')


def public_chat_server(data_path, port=8008):
    """
    Prepare a server that allows staff to chat with IT admins.
    Server runs on port 8008.
    However, users must authenticate to access their chat!
    """
    handlers = [
        (r'/chat/', ChatMainHandler),
        (r'/', tornado.web.RedirectHandler, dict(url=r"/chat/")),
        (r'/login', ChatLoginHandler),
        (r'/logout', ChatLogoutHandler),
        (r'/chat/post', ChatPostHandler),
        (r'/chat/add', ChatCreateHandler),
        (r'/chats/([^/]+)', ChatHandler)
    ]
    settings = dict(
        cookie_secret="1XVMZzBUIbz3m22QUNrrkSDO8gl0014stiEcuDCLt8R4g5EOJM",
        static_path=os.path.join(data_path, "static"),
        xsrf_cookies=True,
        login_url='/login',
        debug=True,
        template_loader=tornado.template.Loader(
                os.path.join(data_path, "templates"),
                namespace = {'cross_secrecy_escape': cross_secrecy_escape,'chat_escape': chat_escape},
                autoescape = 'cross_secrecy_escape', whitespace = 'oneline'
            ),
        title="Cross-Secrecy Chat",
    )
    application = tornado.web.Application(handlers, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port, address='0.0.0.0')

def main():
    options.parse_command_line()
    try:
        logging.debug('Preparing Database')
        database.setup(options.database)

        logging.debug('Preparing Issue-Accept-Server')
        public_issue_server(port=options.port_issueserver)
        logging.debug('Preparing Admin-Webpanel-Server')
        admin_server(options.data, port=options.port_adminpanel)
        logging.debug('Preparing Chat-Server')
        public_chat_server(options.data, port=options.port_chatserver)

        logging.debug('Starting synthetic issue creator')
        issue_scheduler()
        logging.info('Starting Web-Server')
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        logging.warn('Shutting down all servers')
        database.close()
        logging.info('Exited without errors')

if __name__=='__main__':
    main()
