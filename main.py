import cgi
import datetime
from google.appengine.ext import ndb
import webapp2
import json
import array as arr


def get(self):
    self.response.headers.add_header('Access-Control-Allow-Origin', '*')
    self.response.headers['Content-Type'] = 'application/json'
    # do something


def postValue(self):
    self.response.headers.add_header('Access-Control-Allow-Origin', '*')
    self.response.headers['Content-Type'] = 'application/json'
    # do something


def options(self):
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

# -------------------- POST ----------------------


class Post(ndb.Model):
    title = ndb.StringProperty()
    category_id = ndb.IntegerProperty()
    sapo = ndb.StringProperty()
    description = ndb.TextProperty()
    date_joined = ndb.DateTimeProperty(auto_now_add=True)
# ----------------------------------------------------


# -------------------- CATEGORY ----------------------


class Category(ndb.Model):
    nameCategory = ndb.StringProperty()
    date_joined = ndb.DateTimeProperty(auto_now_add=True)


class CategorySubAdd(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

        nameCategory = self.request.get('name')
        if nameCategory != None and nameCategory != '':
            categoryAdd = Category(nameCategory=nameCategory)
            categoryAdd.put()
            self.response.out.write(categoryAdd.key.id())
        else:
            self.response.out.write("Fail")


class CategorySubDelete(webapp2.RequestHandler):
    def post(self):
        idCategory = self.request.get('id')
        ndb.Key("Category", int(idCategory)).delete()
        self.redirect("http://localhost:1962/#categoryview")


class CategorySubEdit(webapp2.RequestHandler):
    def post(self):
        self.options()
        idCategory = self.request.get('id')
        nameToEdit = self.request.get('name')

        if nameToEdit != None and nameToEdit != '' and idCategory != None and idCategory != '':
            categoryEdit = ndb.Key("Category", int(idCategory)).get()
            categoryEdit.nameCategory = nameToEdit
            categoryEdit.put()
            self.response.out.write("Edit Complete")
        else:
            self.response.out.write("Edit Fail")

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'


class CategoryHandler(webapp2.RequestHandler):
    def get(self):
        self.options()
        query = Category.query().fetch()
        names = [
            {
                "name": c.nameCategory,
                "id": c.key.id()
            }
            for c in query]

        self.response.out.write(
            json.dumps(names))

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
# ----------------------------------------------------


app = webapp2.WSGIApplication([
    ('/addCategory', CategorySubAdd),
    ('/deleteCategory', CategorySubDelete),
    ('/editCategory', CategorySubEdit),
    ('/category/json', CategoryHandler),
], debug=True)
