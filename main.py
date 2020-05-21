import cgi
from google.appengine.ext import ndb
import webapp2
import json
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.api import search


class Comment(ndb.Model):
    post_id = ndb.IntegerProperty()
    username = ndb.StringProperty()
    content = ndb.StringProperty()
    date_joined = ndb.DateTimeProperty(auto_now_add=True)


class CommentHandler(webapp2.RequestHandler):
    def post(self):
        self.options()
        username = self.request.get('username')
        post_id = int(self.request.get('post_id'))
        content = self.request.get('content')

        if username != "" and post_id != "" and content != "":
            # Put datastore
            comment_post = Comment(
                username=username,
                post_id=post_id,
                content=content)
            comment_post.put()

            # Put document
            post_document = search.Document(
                doc_id=str(comment_post.key.id()),
                fields=[
                    search.TextField(name="post_id", value=str(post_id)),
                    search.TextField(name="username", value=username),
                    search.TextField(name="content", value=content),
                ]
            )
            # Put post document
            index = search.Index('comment')
            index.put(post_document)

            self.response.out.write(comment_post.key.id())
        else:
            self.response.out.write("Fail")

    def get_by_post_id(self, post_id):
        self.options()
        index = search.Index('comment')
        document = index.search("post_id = {}".format(post_id))

        data_json = [
            {
                "comment_id": comment.fields[0].value,
                "username": comment.fields[1].value,    
                "content": comment.fields[2].value,
            }
            for comment in document
        ]

        self.response.out.write(json.dumps(data_json))

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

# -------------------- POST ----------------------


class Post(ndb.Model):
    title = ndb.StringProperty()
    category_id = ndb.IntegerProperty()
    sapo = ndb.StringProperty()
    image_id = ndb.BlobKeyProperty()
    description = ndb.TextProperty()
    date_joined = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_all(cls):
        return cls.query().fetch()

    @classmethod
    def get_by_id(cls, post_id):
        return ndb.Key(cls, int(post_id)).get()

    @classmethod
    def delete_by_id(cls, post_id):
        # Get post to delete
        post_to_delete = Post.get_by_id(post_id)

        # Delete photo of this post in Blobstore
        blobstore.delete(post_to_delete.image_id)
        # Delete this post
        return ndb.Key(cls, int(post_id)).delete()


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
                "image": str(c.image_id),
            }
            for c in query]

        # write json to file
        self.response.out.write(json.dumps(data_json))

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
                    # Put this post updated
                    postEdit.put()
                    self.response.out.write("Complete")
                else:
                    self.response.out.write(notification)

        else:
            self.response.out.write(
                "Not Found This Post with ID: " + post_id)

    def delete(self):
        self.options()
        try:
            post_id = self.request.get("post_id")
            if post_id is not None:

                # Delete this post
                Post.delete_by_id(int(post_id))
                # Delete this post in document
                index = search.Index('post')
                index.delete(post_id)

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
                "image": str(c.image_id),
            }
            for c in query]

        self.response.out.write(json.dumps(data_json))

    def getByTitle(self, title_post_search):
        self.options()
        query = Post.query().filter(Post.title == title_post_search)
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
                "image": str(c.image_id),
            }
            for c in query]

        self.response.out.write(json.dumps(data_json))

    def get_detail(self, post_id):
        if post_id is not None:
            self.options()
            post_detail = Post.get_by_id(post_id)

            # render file json
            data_json = [
                {
                    "id": post_detail.key.id(),
                    "title": post_detail.title,
                    "sapo": post_detail.sapo,
                    "category": {
                        "id": post_detail.category_id,
                        "label": ndb.Key("Category", int(post_detail.category_id)).get().nameCategory
                    },
                    "date_joined": str(post_detail.date_joined),
                    "description": post_detail.description,
                    "image": str(post_detail.image_id),
                }
            ]
            # write json to file
            self.response.out.write(json.dumps(data_json))
        else:
            return

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'


class AddPost(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        self.options()

        # Put post main
        title = self.request.get('title')
        category_id = self.request.get('category_id')
        sapo = self.request.get('sapo')
        description = self.request.get('description')

        #  put image
        upload = self.get_uploads()[0]

        # put post
        post_add = Post(
            title=title,
            category_id=int(category_id),
            sapo=sapo,
            description=description,
            image_id=upload.key())
        post_add.put()

        # Create document with this post ready to add
        post_document = search.Document(
            doc_id=str(post_add.key.id()),
            fields=[
                search.TextField(name="title", value=title),
                search.TextField(name="category_id", value=str(category_id)),
                search.TextField(name="sapo", value=sapo),
                search.TextField(name="description", value=description),
                search.TextField(name="image_id", value=str(upload.key())),
            ]
        )
        # Put post document
        index = search.Index('post')
        index.put(post_document)

    def get_url(self):
        self.options()
        self.response.out.write(blobstore.create_upload_url('/upload_photo'))

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'


class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        self.options()
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)

    @classmethod
    def delete_by_key(cls, photo_key):
        if blobstore.get(photo_key):
            blobstore.delete(photo_key)

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
    webapp2.Route("/editPost", PostHandler,
                  handler_method="edit", methods=['POST']),

    webapp2.Route("/deletePost", PostHandler,
                  handler_method="delete", methods=['POST']),

    webapp2.Route("/post/json", PostHandler,
                  handler_method="get", methods=['GET']),

    webapp2.Route("/post/detail/<post_id>/json", PostHandler,
                  handler_method="get_detail", methods=['GET']),

    webapp2.Route("/post/title/<title_post_search>/json",
                  PostHandler, handler_method="getByTitle", methods=['GET']),

    webapp2.Route("/post/category/<categoryID_post_search:\d+>/json", PostHandler,
                  handler_method="getByCategory", methods=['GET']),


    # Route Comment
    webapp2.Route("/comment/addComment", CommentHandler,
                  handler_method="post", methods=['POST']),

    webapp2.Route("/comment/get/<post_id>/json", CommentHandler,
                  handler_method="get_by_post_id", methods=['GET']),

    # Rout add
    webapp2.Route("/post/get-url-add", AddPost,
                  handler_method="get_url", methods=['GET']),

    webapp2.Route("/upload_photo", AddPost,
                  handler_method="post", methods=['POST']),

    webapp2.Route('/view_photo/<photo_key>', ViewPhotoHandler,
                  handler_method="get", methods=['GET']),

], debug=True)
