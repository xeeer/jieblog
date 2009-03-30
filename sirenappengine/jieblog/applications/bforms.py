from django import newforms as forms
from google.appengine.api import users
import models
from google.appengine.ext.db import djangoforms
from funcs import split_tags,get_cat

CODE_LICENSE_CHOICES = (
	('Artistic License/GPL', 'Artistic License/GPL'),
	('Apache License 2.0', 'Apache License 2.0'),
	('Eclipse Public License 1.0', 'Eclipse Public License 1.0'),
	('GNU General Public License v2', 'GNU General Public License v2'),
	('GNU General Public License v3', 'GNU General Public License v3'),
	('GNU Lesser General Public License', 'GNU Lesser General Public License'),
	('MIT License', 'MIT License'),
	('Mozilla Public License 1.1', 'Mozilla Public License 1.1'),
	('New BSD License', 'New BSD License'),
)

CONTENT_LICENSE_CHOICES = (
	('Creative Commons 3.0 BY', 'Creative Commons 3.0 BY'),
	('Creative Commons 2.0 BY-SA', 'Creative Commons 2.0 BY-SA'),
)

class SiteForm(forms.Form):
	site_title = forms.CharField()
	sub_title = forms.CharField()
	site_copyright = forms.CharField()
	post_per_page = forms.IntegerField(max_value=30,min_value=1)
	owner_name = forms.CharField()
	code_license = forms.ChoiceField(choices=CODE_LICENSE_CHOICES)
	content_license = forms.ChoiceField(choices=CONTENT_LICENSE_CHOICES)


	def save(self,site):
		site.site_title = self.clean_data['site_title']
		site.sub_title = self.clean_data['sub_title']
		site.site_copyright = self.clean_data['site_copyright']
		site.post_per_page = self.clean_data['post_per_page']
		site.owner_name = self.clean_data['owner_name']
		site.code_license = self.clean_data['code_license']
		site.content_license = self.clean_data['content_license']
		site.put()

class CatForm(forms.Form):
	name = forms.CharField()
	slug = forms.CharField()
	def save(self):
		cat = models.Cat(name=self.clean_data['name'],slug=self.clean_data['slug'])
		cat.put()
	def edit(self,cat):
		cat.name=self.clean_data['name']
		cat.slug=self.clean_data['slug']
		cat.put()

class ConfigForm(forms.Form):
	name = forms.CharField()
	subtitle = forms.CharField()
	post_per_page = forms.CharField()
	
	def save(self):
		configdb = models.ConfigDB(name=self.clean_data['name'],subtitle=self.clean_data['subtitle'],post_per_page=self.clean_data['post_per_page'])
		configdb.put()
	def safe(self,configdb):
		configdb.name=self.clean_data['name']
		configdb.subtitle=self.clean_data['subtitle']
		configdb.post_per_page=self.clean_data['post_per_page']
		configdb.put()
	
class PostForm(forms.Form):
	article = forms.BooleanField(required=False)
	draft = forms.BooleanField(required=False,label='Publish')
	title = forms.CharField()
	slug = forms.CharField()
	cat = djangoforms.ModelChoiceField(models.Cat,required=True,query=models.Cat.all())
	tags = forms.CharField()
	content = forms.CharField(widget=forms.Textarea())

	def save(self,currnet_user):
		tags = split_tags(self.clean_data['tags'])
		for tag in tags:
			query = models.BlogTag.all().filter('name =',tag)
			thetag = query.get()			
			if thetag==None:
				blogtag = models.BlogTag(name=tag)
				blogtag.put()
		post = models.Post(cat=self.clean_data['cat'],slug=self.clean_data['slug'],article=self.clean_data['article'],tags = tags,title = self.clean_data['title'],content = self.clean_data['content'],author = currnet_user,draft = self.clean_data['draft'])
		post.put()


class EditForm(forms.Form):
	article = forms.BooleanField(required=False)
	draft = forms.BooleanField(required=False,label='Publish')
	title = forms.CharField()
	slug = forms.CharField()
	cat = djangoforms.ModelChoiceField(models.Cat,required=True,query=models.Cat.all())
	tags = forms.CharField()
	content = forms.CharField(widget=forms.Textarea())
	def save(self,post):
		post.title = self.clean_data['title']
		post.content = self.clean_data['content']
		post.tags = split_tags(self.clean_data['tags'])
		post.article = self.clean_data['article']
		post.draft = self.clean_data['draft']
		post.slug = self.clean_data['slug']
		post.cat= self.clean_data['cat']
		post.put()
		
			
		
class CommentForm(forms.Form):	
	comments_author = forms.EmailField(initial='@',label='Your Email')
	comments_author_url = forms.URLField(initial='http://',label='Your Home Page')
	comments_content = forms.CharField(widget=forms.Textarea(),label='Say Something')	
	def save(self,post_key):
		comments_author = self.clean_data['comments_author']
		comments_author_url = self.clean_data['comments_author_url']
		user = users.User(comments_author)
		query = models.JieBlogUser.all().filter('user_name =',comments_author)
		jiebloguser = query.get()
		if jiebloguser == None:
			jiebloguser = models.JieBlogUser(user_name=user,user_url=comments_author_url)
			jiebloguser.put()		
		comment = models.Comments(comments_author_class=jiebloguser,comments_author_link=comments_author_url,post = post_key,comments_author=user,comments_content = self.clean_data['comments_content'])
		comment.put()

class CommentFormUser(forms.Form):
	comments_author_url = forms.URLField(label='Your Home Page')
	comments_content = forms.CharField(widget=forms.Textarea())	
	def save(self,post_key,user):
		query = models.JieBlogUser.all().filter('user_name =',user)
		comments_author_url = self.clean_data['comments_author_url']
		jiebloguser = query.get()
		if jiebloguser == None:
			jiebloguser = models.JieBlogUser(user_name=user,user_url=comments_author_url)
		else:
			jiebloguser.user_url = comments_author_url
		jiebloguser.put()	
		comment = models.Comments(comments_author_link=comments_author_url,comments_author_class=jiebloguser,post = post_key,comments_author = user, comments_content = self.clean_data['comments_content'])
		comment.put()		

class SiteLinkForm(forms.Form):
	sitelinkform_title = forms.CharField()
	sitelinkform_link = forms.URLField()
	sitelinkform_summary = forms.CharField(widget=forms.Textarea())
	def save(self):
		sitelink = models.SiteLink(title=self.clean_data['sitelinkform_title'],link=self.clean_data['sitelinkform_link'],summary=self.clean_data['sitelinkform_summary'])
		sitelink.put();
		
class FeatureLinkForm(forms.Form):
	title = forms.CharField()
	link = forms.URLField()
	summary = forms.CharField(widget=forms.Textarea())
	def save(self):
		featurelink = models.FeatureLink(link=self.clean_data['link'],title=self.clean_data['title'],summary=self.clean_data['summary'])
		featurelink.put();
		
class EditFeatureForm(forms.Form):
	title = forms.CharField()
	link = forms.URLField()
	summary = forms.CharField(widget=forms.Textarea())
	def save(self,feature_item):		
		feature_item.title = self.clean_data['title']
		feature_item.summary = self.clean_data['summary']
		feature_item.link = self.clean_data['link']
		feature_item.put()
		
class QuotationForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea())
	author = forms.CharField()
	wow = forms.BooleanField(required=False)
	link = forms.URLField(required=False)
	tclass= forms.CharField()
	def save(self):
		quotation = models.Quotation(tclass=self.clean_data['tclass'],link=self.clean_data['link'],content=self.clean_data['content'],author=self.clean_data['author'],wow =self.clean_data['wow'])
		quotation.put();
		
class EditQuotationForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea())
	author = forms.CharField()
	wow = forms.BooleanField(required=False)
	link = forms.URLField(required=False)
	tclass= forms.CharField()
	def save(self,quotation):		
		quotation.content = self.clean_data['content']
		quotation.author = self.clean_data['author']
		quotation.link = self.clean_data['link']
		quotation.wow = self.clean_data['wow']
		quotation.tclass=self.clean_data['tclass']
		quotation.put()

