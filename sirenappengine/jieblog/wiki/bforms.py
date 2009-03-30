from django import newforms as forms
from google.appengine.api import users
import models
from google.appengine.ext.db import djangoforms
from funcs import split_tags,get_cat

class WikiForm(forms.Form):
	title = forms.CharField()
	content = forms.CharField(widget=forms.Textarea())
	slug = forms.CharField()
	
	
	def save(self):
		current_user = users.get_current_user()
		wiki = models.Wiki(
							title=self.clean_data['title'],
							content=self.clean_data['content'],
							slug=self.clean_data['slug'],
							author=current_user,
							)
		wiki.put()
	def edit(self,wiki):
		wiki.title=self.clean_data['title']
		wiki.content=self.clean_data['content']
		wiki.slug=self.clean_data['slug']
		wiki.put()
