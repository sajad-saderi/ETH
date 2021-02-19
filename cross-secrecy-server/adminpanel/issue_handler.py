import tornado.web
from tornado.escape import json_decode
from datetime import datetime
import logging

try:
    import database
    from issue import Issue
except ImportError:
    import adminpanel.database as database
    from adminpanel.issue import Issue

class IssueHandler(tornado.web.RequestHandler):
    async def get(self, slug):
        self.xsrf_token # accessing this variable makes it do a 'set-cookie' if unset
        issue_id = int(slug)
        issue = database.get_issue(issue_id)
        if issue is None:
            return self.render("404.html", error='Issue with id {} not found.'.format(issue_id))
        self.render("issue.html", issue=issue)

class IssueImageHandler(tornado.web.RequestHandler):
    async def get(self, slug):
        issue_id = int(slug)
        issue = database.get_issue(issue_id)
        if issue is None:
            return self.render("404.html", error='Issue with id {} not found.'.format(issue_id))
        self.write(issue.image)

class IssuesHandler(tornado.web.RequestHandler):
    async def get(self):
        issues = database.get_issue()
        self.render("issues.html", issues=issues)

class IssueRemoveHandler(tornado.web.RequestHandler):
    async def delete(self, slug):
        issue_id = int(slug)
        logging.info('Removing issue with ID {}'.format(issue_id))
        database.remove_issue(issue_id)

class IssuePostHandler(tornado.web.RequestHandler):
    async def post(self):
        self.args = json_decode(self.request.body)
        author = self.args['author']
        subject = self.args['subject']
        description = self.args['description']
        image = self.args['image']
        date = str(datetime.now())
        id_ = database.get_next_id()
        issue = Issue(author,subject,description,image,id=id_,date=date)

        logging.info('Received new issue from {}'.format(author))
        #except NoResultError:
        #    raise tornado.web.HTTPError(500)
        database.commit_issue(issue)
