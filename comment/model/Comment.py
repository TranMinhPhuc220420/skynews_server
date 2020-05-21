import cgi
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import search

class Comment(ndb.Model):
  post_id = ndb.IntegerProperty()
  username  = ndb.StringProperty()
  content = ndb.StringProperty()
  date_joined = ndb.DateTimeProperty(auto_now_add=True)