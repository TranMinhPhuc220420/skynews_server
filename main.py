import cgi
from google.appengine.ext import ndb
import webapp2
import json

class Image(ndb.Model):
    image = ndb.BlobProperty()
    date_joined = ndb.DateTimeProperty(auto_now_add=True)


class ImageHandler (webapp2.RequestHandler):
    def get(self, image_id):
        self.options()
        image_post = ndb.Key("Image", int(image_id)).get()
        if image_post.image:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(image_post.image)
        else:
            self.response.out.write('No image')

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

# -------------------- POST ----------------------


class Post(ndb.Model):
    title = ndb.StringProperty()
    category_id = ndb.IntegerProperty()
    sapo = ndb.StringProperty()
    image_id = ndb.IntegerProperty()
    description = ndb.TextProperty()
    date_joined = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_all(cls):
        return cls.query().fetch()


class PostHandler(webapp2.RequestHandler):
    def get(self):
        self.options()
        # get all post
        query = Post.get_all()

        # render file json
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
                "image": c.image_id,
            }
            for c in query]

        # write json to file
        self.response.out.write(json.dumps(data_json))

    def post(self):
        self.options()

        # Put post main
        title = self.request.get('title')
        category_id = self.request.get('category_id')
        image = "https://i.picsum.photos/id/1015/6000/4000.jpg"
        sapo = self.request.get('sapo')
        description = self.request.get('description')

        image_upload = self.request.get('image')

        # Check before adding
        if title != None and title != '':
            if category_id != None and category_id != '':
                if image_upload != None and image_upload != '':
                    if sapo != None and sapo != '':
                        if description != None and description != '':

                            # # upload image_upload
                            if image_upload != None:
                                #  put image
                                subImageUpload = Image(image=image_upload)
                                subImageUpload.put()

                                # put post
                                post_add = Post(title=title, category_id=int(
                                    category_id), sapo=sapo, description=description, image_id=subImageUpload.key.id())
                                post_add.put()

                                # Notification
                                self.response.out.write("Completed")
                            else:
                                self.response.out.write("None image")


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

    def edit(self):
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

    def delete(self):
        self.options()
        post_delete = ndb.Key("Post", int(self.request.get('post_id')))
        try:
            if post_delete is not None:
                post_delete.delete()
                self.response.out.write("Complete")
            else:
                self.response.out.write("Delete Fail")
        except:
            self.response.out.write("Delete Fail\nSome wrong in server")

    def getByCategory(self, categoryID_post_search):
        self.options()
        query = Post.query(Post.category_id == int(categoryID_post_search))
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
                "image": c.image_id,
            }
            for c in query]

        self.response.out.write(json.dumps(data_json))

    def getByTitle(self, title_post_search):
        self.response.out.write(title_post_search)

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
# ----------------------------------------------------


# -------------------- CATEGORY ----------------------

class Category(ndb.Model):
    nameCategory = ndb.StringProperty()
    date_joined = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_all(cls):
        return cls.query().fetch()


class CategoryHandler(webapp2.RequestHandler):
    def get(self):
        self.options()
        # get all category
        query = Category.get_all()

        # render file json
        data_json = [
            {
                "name": c.nameCategory,
                "id": c.key.id()
            }
            for c in query]

        # write json to file
        self.response.out.write(json.dumps(data_json))

    def post(self):
        self.options()
        nameCategory = self.request.get('name')
        if nameCategory != None and nameCategory != '':
            categoryAdd = Category(nameCategory=nameCategory)
            categoryAdd.put()
            self.response.out.write(categoryAdd.key.id())
        else:
            self.response.out.write("Fail")

    def edit(self):
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

    def delete(self):
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
# ----------------------------------------------------


app = webapp2.WSGIApplication([
    # Route category
    webapp2.Route('/addCategory', CategoryHandler,
                  handler_method="post", methods=['POST']),

    webapp2.Route('/deleteCategory', CategoryHandler,
                  handler_method="delete", methods=['POST']),

    webapp2.Route('/editCategory', CategoryHandler,
                  handler_method="edit", methods=['POST']),

    webapp2.Route('/category/json', CategoryHandler,
                  handler_method="get", methods=['GET']),


    # Route post
    webapp2.Route("/addPost", PostHandler,
                  handler_method="post", methods=['POST']),

    webapp2.Route("/editPost", PostHandler,
                  handler_method="edit", methods=['POST']),

    webapp2.Route("/deletePost", PostHandler,
                  handler_method="delete", methods=['POST']),

    webapp2.Route("/post/json", PostHandler,
                  handler_method="get", methods=['GET']),

    webapp2.Route("/post/title/<title_post_search>/json",
                  PostHandler, handler_method="getByTitle", methods=['GET']),

    webapp2.Route("/post/category/<categoryID_post_search:\d+>/json", PostHandler,
                  handler_method="getByCategory", methods=['GET']),

    # Route image
    webapp2.Route("/image/post/<image_id>", ImageHandler,
                  handler_method="get")
], debug=True)
