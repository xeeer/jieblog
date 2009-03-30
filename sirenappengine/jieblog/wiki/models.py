from google.appengine.ext import db
import datetime
import hashlib,urllib

class Wiki(db.Model):
	title = db.StringProperty(required=True)
	content = db.TextProperty()
	author = db.UserProperty()	
	post_on = db.DateTimeProperty(auto_now_add=True)
	edit_on = db.DateTimeProperty(auto_now=True)
	slug =  db.StringProperty(multiline=False)
	
	def __str__ (self):
		return '%s' %self.title
		
	def get_absolute_url(self):
		return '%s' %self.key().id()
