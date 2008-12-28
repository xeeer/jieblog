from django.http import HttpResponse, HttpResponseRedirect
from jieblog.applications import models
from jieblog.applications import bforms
from google.appengine.api import users
from google.appengine.ext import db
import random
from funcs import render, getcached
from google.appengine.api import urlfetch
from xml.dom import minidom
import urllib2
from datetime import datetime


def edit_feature(request,feature_list_id):
	user = users.get_current_user()
	if users.is_current_user_admin():
		feature_item = models.FeatureLink.get_by_id(int(feature_list_id))
		editfeatureform = bforms.EditFeatureForm(initial={'title':feature_item.title,'realized':feature_item.realized,'summary':feature_item.summary})
		if request.method == 'POST':
			editfeatureform = bforms.EditFeatureForm(request.POST)
			if editfeatureform.is_valid():
				editfeatureform.save(feature_item)
				return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/404.html')
	payload = dict(editfeatureform=editfeatureform)
	return render('edit_feature_list.html', payload)
	
def edit_quotation(request,quotation_id):
	user = users.get_current_user()
	if users.is_current_user_admin():		
		quotation = models.Quotation.get_by_id(int(quotation_id))
		editquotationform = bforms.EditQuotationForm(initial={'tclass':quotation.tclass,'content':quotation.content,'link':quotation.link,'author':quotation.author,'wow':quotation.wow})
		if request.method == 'POST':
			editquotationform = bforms.EditQuotationForm(request.POST)
			if editquotationform.is_valid():
				editquotationform.save(quotation)
				return HttpResponseRedirect('/quotation')
	else:
		return HttpResponseRedirect('/404.html')
	payload = dict(quotationform=editquotationform)
	return render('addquotation.html', payload)

def view_tag(request,post_tag):
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
#	all_posts = models.Post.all().filter('draft',True).order('-post_on')
	all_posts = getcached('Post', lambda: models.Post.all().filter('draft',True).order('-post_on'), expiration=3600)
	tag_posts = []
	for post in all_posts:
		if post_tag in post.tags:
			tag_posts.append(post)			
#	comments = models.Comments.all()
	recent_comments= getcached('Comments', lambda: models.Comments.all().order('-comments_post_on').fetch(5), expiration=3600)
#	recent_comments = comments.order('-comments_post_on').fetch(5)
#	sitelink = models.SiteLink.all()
	sitelink = getcached('SiteLink', lambda: models.SiteLink.all(), expiration=3600)
#	featurelink = models.FeatureLink.all()
	featurelink = getcached('FeatureLink', lambda: models.FeatureLink.all(), expiration=3600)
#	tag_cloud = models.BlogTag.all()
	tag_cloud = getcached('BlogTag', lambda: models.BlogTag.all(), expiration=3600)
#	articles =  models.Post.all().filter('article',True)
	articles = all_posts.filter('article',True)
	payload = dict(recent_comments=recent_comments,featurelink=featurelink,tag_cloud=tag_cloud,sitelink=sitelink,tag_posts = tag_posts,greeting=greeting,show_edit=show_edit)
	return render('tag.html',payload)
			

def feeds(request):
	posts =  getcached('Post', lambda: models.Post.all(), expiration=3600)
	latest_post = posts[posts.count()-1]
	posts.order('-post_on')
	payload = dict(posts = posts,latest_post = latest_post)
	return render('atom.xml',payload)
	
def sitemap(request):
	posts =  getcached('Post', lambda: models.Post.all(), expiration=3600)
	latest_post = posts[posts.count()-1]
	posts.order('-post_on')
	payload = dict(posts = posts,latest_post = latest_post)
	return render('feed.xml',payload)

def index(request,page=0):
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
	page = int(page)
	posts_per_page = 6
	show_prev = False
	show_next = False
#	all_posts = models.Post.all()
	all_posts = getcached('Post', lambda: models.Post.all(), expiration=3600)
	max_page = (all_posts.count()-1) / posts_per_page
	posts = all_posts.filter('draft',True).order('-post_on').fetch(posts_per_page, offset = page * posts_per_page)
	show_prev = not (page == 0)
	show_next = not (page == max_page)
	if not posts:
		show_prev = False
		show_next = False
	current_page = page + 1

#	comments = models.Comments.all()
	recent_comments= getcached('Comments', lambda: models.Comments.all().order('-comments_post_on').fetch(5), expiration=3600)
#	recent_comments = comments.order('-comments_post_on').fetch(5)
#	sitelink = models.SiteLink.all()
	sitelink = getcached('SiteLink', lambda: models.SiteLink.all(), expiration=3600)
#	featurelink = models.FeatureLink.all()
	featurelink = getcached('FeatureLink', lambda: models.FeatureLink.all(), expiration=3600)
#	tag_cloud = models.BlogTag.all()
	tag_cloud = getcached('BlogTag', lambda: models.BlogTag.all(), expiration=3600)
#	articles =  models.Post.all().filter('article',True)
	articles = all_posts.filter('article',True)
	friendsconnect = True

	payload = dict(recent_comments=recent_comments,friendsconnect=friendsconnect,articles=articles,featurelink=featurelink,tag_cloud=tag_cloud,sitelink=sitelink,show_edit=show_edit,greeting=greeting,posts = posts,show_prev = show_prev,show_next = show_next,show_page_panel = show_prev or show_next,prev = page - 1,next = page + 1,current_page = current_page)
	return render('index.html', payload)

def comment(request, post_id):
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
	post = models.Post.get_by_id(int(post_id))
	comments = models.Comments.all().filter("post",post)		
	if user:
		if request.method == 'POST':
			commentform = bforms.CommentFormUser(request.POST)
			if commentform.is_valid():				
				comment = commentform.save(post,user)
				return HttpResponseRedirect('/post/%s'%post_id)
		else:
			commentform = bforms.CommentFormUser()
	else:
		if request.method == 'POST':
			commentform = bforms.CommentForm(request.POST)
			if commentform.is_valid():				
				comment = commentform.save(post)
				return HttpResponseRedirect('/post/%s'%post_id)
		else:
			commentform = bforms.CommentForm()
	
	sitelink = models.SiteLink.all()
	featurelink = models.FeatureLink.all()
	tag_cloud = models.BlogTag.all()
	articles =  models.Post.all().filter('article',True)
	friendsconnect = False
	payload = dict(friendsconnect=friendsconnect,articles=articles,featurelink=featurelink,tag_cloud=tag_cloud,sitelink=sitelink,greeting=greeting,show_edit=show_edit,post=post,commentform=commentform,comments=comments)
	return render('comment.html', payload)
	
def site_link(request):
	sitelink = models.SiteLink.all()
	payload = dict(sitelink=sitelink)
	return render('sitelink.html', payload)
	
def add_feature_link(request):
	user = users.get_current_user()
	if users.is_current_user_admin():
		if request.method == 'POST':
			featurelinkform = bforms.FeatureLinkForm(request.POST)
			if featurelinkform.is_valid():
				featurelinkform.save()
				return HttpResponseRedirect('/')	
		else:
			featurelinkform = bforms.FeatureLinkForm()
	else:
		return HttpResponseRedirect('/')	
	payload = dict(featurelinkform=featurelinkform)
	return render('featurelinkadmin.html', payload)
	
def quotation(request):
	user = users.get_current_user()
	quotations = models.Quotation.all()
	quotationform = bforms.QuotationForm()
	if user:
		greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
				  (user.nickname(), users.create_logout_url("/")))			
	else:
		greeting = ("<a href=\"%s\">Sign in or register</a>." %
				  users.create_login_url("/"))
	if users.is_current_user_admin():
		show_edit =True
		if request.method == 'POST':
			quotationform = bforms.QuotationForm(request.POST)
			if quotationform.is_valid():
				quotationform.save()
				return HttpResponseRedirect('/quotation')	
	else:
		show_edit =False	
	payload = dict(quotations=quotations,show_edit=show_edit,quotationform=quotationform)
	return render('quotation.html',payload)

def feature_link(request):
	featurelink = models.FeatureLink.all()
	payload = dict(featurelink=featurelink)
	return render('featurelink.html', payload)

def uploader(request,pic_key=None):
	user = users.get_current_user()
	if user:
		greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
				  (user.nickname(), users.create_logout_url("/")))			
	else:
		greeting = ("<a href=\"%s\">Sign in or register</a>." %
				  users.create_login_url("/"))
	if user:
		if request.method == 'POST':			
			for f,file_info in request.FILES.items():
				fu = models.FileUpload(filename=file_info['filename'],
					content_type=file_info['content-type'],
					content=db.Blob(file_info['content']),
					owner=users.get_current_user(),
					size=len(db.Blob(file_info['content'])))				
			fu.put()
			return HttpResponseRedirect('/uploader')	
	userfiles = models.FileUpload.all()
	payload = dict(userfiles=userfiles,user=user,greeting=greeting)
	return render('upload.html', payload)
	
def filelist(request):
	user = users.get_current_user()
	if user:
		greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
				  (user.nickname(), users.create_logout_url("/")))			
	else:
		greeting = ("<a href=\"%s\">Sign in or register</a>." %
				  users.create_login_url("/"))	
	userfiles = models.FileUpload.all()
	payload = dict(userfiles=userfiles,user=user,greeting=greeting)
	return render('filelist.html',payload)
	
def filedown(request,the_key):
	the_file = models.FileUpload.get(the_key)
	response = HttpResponse(the_file.content)
	response['Content-Type'] = the_file.content_type	
	#response['Content-Disposition'] = 'attachment; filename=%s'%the_file.filename #remove the can get a paste pic
	return response

def filedelete(request,the_key):
	the_file = models.FileUpload.get(the_key)
	user = users.get_current_user()
	if the_file and the_file.owner == user or users.is_current_user_admin():
		the_file.delete()
	return HttpResponseRedirect('/filelist')