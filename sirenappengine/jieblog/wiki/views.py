from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import ObjectPaginator, InvalidPage

from jieblog.wiki import models
from jieblog.wiki import bforms
from google.appengine.api import users
from google.appengine.ext import db
import random
from funcs import render, getcached
from wikimarkup import parselite
from google.appengine.api import urlfetch
from xml.dom import minidom
import urllib2
from datetime import datetime

def wiki(request):
	user = users.get_current_user()
	if user:
		greeting = ("<a href=\"%s\">Sign Out</a>" %
				  (users.create_logout_url("/")))			
	else:
		greeting = ("<a href=\"%s\">Sign in</a>" %
				  users.create_login_url("/"))
	if users.is_current_user_admin():
		show_edit = True
	else:
		show_edit = False
	wikiz = models.Wiki.all()
	for wiki in wikiz:
		wiki_text=parselite(wiki.content)
	payload = dict(wiki_text=wiki_text)
	return render('wiki.html', payload)

def write_wiki(request):
	user = users.get_current_user()
	if users.is_current_user_admin():
		if request.method == 'POST':
			wikiform = bforms.WikiForm(request.POST)
			if wikiform.is_valid():
				wiki = wikiform.save()
				return HttpResponseRedirect('/wiki')
		else:
			wikiform = bforms.WikiForm()
	else:
		return  HttpResponseRedirect('/login')
	payload = dict(wikiform = wikiform)
	return render('AdminWiki.html', payload)