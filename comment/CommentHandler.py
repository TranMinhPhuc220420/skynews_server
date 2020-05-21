import cgi
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import search

from model import Comment


class CommentHandler(webapp2.RequestHandler):
    def post(self):
        self.options()
        username = self.request.get('username')
        post_id = self.request.get('post_id')
        content = self.request.get('content')

        if username != None and post_id != None and content != None:
            comment_post = Comment(
                username=username, post_id=post_id, content=content)
            comment_post.put()
            self.response.out.write("Complete")
        else:
            self.response.out.write("Fail")

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
