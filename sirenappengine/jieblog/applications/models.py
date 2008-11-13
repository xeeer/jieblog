from google.appengine.ext import db
import hashlib,urllib

class ConfigDB(db.Model):
	name = db.StringProperty()
	subtitle = db.StringProperty()
	post_per_page = db.StringProperty()
	
	def get_config_url (self):
		return '%s' %self.key().id()

class BlogTag(db.Model):
	name = db.StringProperty()
	def __str__ (self):
		return '%s' %self.name
		
	def get_tag_url (self):
		return '%s' %self.name

class JieBlogUser(db.Model):
	user_name = db.UserProperty()
	user_url = db.LinkProperty()
	
class SiteLink(db.Model):
	title = db.StringProperty()
	link = db.LinkProperty(required=True)
	summary = db.TextProperty()

class FeatureLink(db.Model):
	title = db.StringProperty()
	realized = db.BooleanProperty()
	summary = db.TextProperty()
	post_on = db.DateTimeProperty(auto_now_add=True)
	
	def get_feature_url (self):
		return '%s' %self.key().id()
		
class Quotation(db.Model):
	post_on = db.DateTimeProperty(auto_now_add=True)
	content = db.TextProperty()
	author = db.StringProperty()
	wow = db.BooleanProperty()
	link = db.LinkProperty()
	tclass = db.StringProperty()
	
	def get_quotation_url (self):
		return '%s' %self.key().id()

class Post(db.Model):
	title = db.StringProperty(required=True)
	content = db.TextProperty()
	author = db.UserProperty()	
	post_on = db.DateTimeProperty(auto_now_add=True)	
	tags = db.StringListProperty()
	comments_count = db.IntegerProperty(0)
	article = db.BooleanProperty()
	draft = db.BooleanProperty(default=False)
	
	def __str__ (self):
		return '%s' %self.title
		
	def get_absolute_url (self):
		return '%s' %self.key().id()
		
	def get_comments_count(self):
		return Comments.all().filter("post",self).count()
			
class Comments(db.Model):
	post = db.ReferenceProperty(Post)
	comments_author_class = db.ReferenceProperty(JieBlogUser)
	comments_author = db.UserProperty()
	comments_content = db.TextProperty()
	comments_author_link = db.LinkProperty()
	comments_post_on = db.DateTimeProperty(auto_now_add=True)
	def get_comments_nickname(self):
		return self.comments_author.nickname()
	def get_gravatar_url(self):
		gravatar_image = "http://www.gravatar.com/avatar.php?"
		enmail = str(self.comments_author.email())
		default = "http://blzinsider.cn/icons/38.png"
		size = 16
		gravatar_image += urllib.urlencode({'gravatar_id':hashlib.md5(enmail).hexdigest(),'default':default,'size':str(size)})
		return gravatar_image

class FileUpload(db.Model):
	owner = db.UserProperty()
	filename = db.StringProperty()
	content_type = db.StringProperty()
	content = db.BlobProperty()
	size = db.IntegerProperty()
	date_added = db.DateProperty(auto_now_add=True)

