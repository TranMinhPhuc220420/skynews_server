import cgi
import datetime
from google.appengine.ext import ndb
import webapp2
import json
import array as arr
import datetime


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
    image = ndb.StringProperty()
    sapo = ndb.StringProperty()
    description = ndb.TextProperty()
    date_joined = ndb.DateTimeProperty(auto_now_add=True)
# ----------------------------------------------------


class PostSubAdd(webapp2.RequestHandler):
    def post(self):
        self.options()
        # Put post main
        title = self.request.get('title')
        category_id = self.request.get('category_id')
        image = "https://i.picsum.photos/id/0/5616/3744.jpg"
        sapo = self.request.get('sapo')
        description = self.request.get('description')

        # Check before adding
        if title != None and title != '':
            if category_id != None and category_id != '':
                if image != None and image != '':
                    if sapo != None and sapo != '':
                        if description != None and description != '':
                            post_add = Post(title=title, category_id=int(category_id), sapo=sapo, description=description,
                                            image=image)
                            post_add.put()
                            self.response.out.write("Completed")
                        else:
                            self.response.out.write(
                                "Fail because of none description")
                    else:
                        self.response.out.write("Fail because of none sapo")
                else:
                    self.response.out.write("Fail because of none image")
            else:
                self.response.out.write("Fail because of none category_id")
        else:
            self.response.out.write("Fail because of none title")

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'


class PostGetAll(webapp2.RequestHandler):
    def get(self):
        self.options()
        query = Post.query().fetch()

        data_json = [
            {
                "id": c.key.id(),
                "title": c.title,
                "sapo": c.sapo,
                "category": {
                    "id": c.category_id,
                    "label": ndb.Key("Category", int(c.category_id)).get().nameCategory
                },
                "date_joined": str(c.date_joined),
                "description": c.description,
                "image": c.image,
            }
            for c in query]

        self.response.out.write(
            json.dumps(data_json))

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'


class PostSubEdit(webapp2.RequestHandler):
    def post(self):
        self.options()

        # Put post main
        post_id = self.request.get('id')
        title = self.request.get('title')
        category_id = self.request.get('category_id')
        sapo = self.request.get('sapo')
        description = self.request.get('description')
        notification = ''
        editSusses = True
        if post_id != None and post_id != '':
            postEdit = ndb.Key("Post", int(post_id)).get()

            # Check before adding
            if postEdit != None and postEdit != '':
                if title != None and title != '':
                    postEdit.title = title
                else:
                    notification += "Fail because of none title\n"
                    editSusses = False

                if category_id != None and category_id != '':
                    postEdit.category_id = int(category_id)
                else:
                    notification += "Fail because of none category_id"
                    editSusses = False

                if sapo != None and sapo != '':
                    postEdit.sapo = sapo
                else:
                    notification += "Fail because of none sapo"
                    editSusses = False

                if description != None and description != '':
                    postEdit.description = description
                else:
                    notification += "Fail because of none description"
                    editSusses = False

                if editSusses == True:
                    postEdit.put()
                    self.response.out.write("Complete")
                else:
                    self.response.out.write(notification)

        else:
            self.response.out.write(
                "Not Found This Post with ID: " + post_id)

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

# -------------------- CATEGORY ----------------------


class Category(ndb.Model):
    nameCategory = ndb.StringProperty()
    date_joined = ndb.DateTimeProperty(auto_now_add=True)


class CategorySubAdd(webapp2.RequestHandler):
    def post(self):
        self.options()

        nameCategory = self.request.get('name')
        if nameCategory != None and nameCategory != '':
            categoryAdd = Category(nameCategory=nameCategory)
            categoryAdd.put()
            self.response.out.write(categoryAdd.key.id())
        else:
            self.response.out.write("Fail")

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'


class CategorySubDelete(webapp2.RequestHandler):
    def post(self):
        self.options()

        idCategory = int(self.request.get('id'))
        if Post.query(Post.category_id == idCategory).get() == None:
            if idCategory != None and idCategory != '':
                ndb.Key("Category", idCategory).delete()
                self.response.out.write("Delete complete")
            else:
                self.response.out.write("Delete  Fail")
        else:
            self.response.out.write("A post have this category\nFail delete")

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'


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


class CategoryGetAll(webapp2.RequestHandler):
    def get(self):
        self.options()
        query = Category.query().fetch()
        data_json = [
            {
                "name": c.nameCategory,
                "id": c.key.id()
            }
            for c in query]

        self.response.out.write(
            json.dumps(data_json))

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
# ----------------------------------------------------


app = webapp2.WSGIApplication([
    # Route category
    webapp2.Route('/addCategory', CategorySubAdd),
    webapp2.Route('/deleteCategory', CategorySubDelete),
    webapp2.Route('/editCategory', CategorySubEdit),
    webapp2.Route('/category/json', CategoryGetAll),

    # Route post
    webapp2.Route("/addPost", PostSubAdd),
    webapp2.Route("/editPost", PostSubEdit),
    webapp2.Route("/post/json", PostGetAll),
], debug=True)
