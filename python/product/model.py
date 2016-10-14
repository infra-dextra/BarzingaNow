from google.appengine.ext import ndb, db

class Product(ndb.Model):
    description = ndb.StringProperty()
    price = ndb.FloatProperty()
    quantity = ndb.IntegerProperty()
    image_url = ndb.StringProperty()
