from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import ObjectPaginator, InvalidPage

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

def tags(request,post_tag):
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

	all_posts = getcached('Post', lambda: models.Post.all(), expiration=3600)
	all_posts = all_posts.filter('draft',True).order('-post_on')
	posts = []
	for post in all_posts:
		if post_tag in post.tags:
			posts.append(post)
	recent_comments= getcached('Comments', lambda: models.Comments.all().order('-comments_post_on').fetch(5), expiration=3600)
	sitelink = getcached('SiteLink', lambda: models.SiteLink.all(), expiration=3600)
	featurelink = getcached('FeatureLink', lambda: models.FeatureLink.all(), expiration=3600)
	tag_cloud = getcached('BlogTag', lambda: models.BlogTag.all(), expiration=3600)
	articles = all_posts.filter('article',True)
	cats=models.Cat.all()
	payload = dict(cats=cats,
					recent_comments=recent_comments,
					featurelink=featurelink,
					tag_cloud=tag_cloud,
					sitelink=sitelink,
					posts = posts,
					greeting=greeting,
					show_edit=show_edit,
					blog_view = 'tag')
	return render('index.html',payload)
	
def feeds(request):
	posts =  getcached('Post', lambda: models.Post.all(), expiration=3600)
	latest_post = posts[posts.count()-1]
	posts.order('-post_on')
	payload = dict(posts = posts,latest_post = latest_post)
	return render('atom.xml',payload)
	
def sitemap(request):
	posts =  getcached('Post', lambda: models.Post.all(), expiration=3600)
	cats = models.Cat.all()
	latest_post = posts[posts.count()-1]
	posts = posts.order('-post_on').fetch(10)	
	payload = dict(cats = cats,posts = posts,latest_post = latest_post)
	return render('feed.xml',payload)

def archive(request,post_year,post_month):
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
	post_year = int(post_year)
	post_month = int(post_month)
	all_posts = getcached('Post', lambda: models.Post.all(), expiration=3600)
	# The very beginning of month N-1
	prevM = datetime((post_year if post_month != 1 else post_year-1),(post_month-1 if post_month != 1 else 12), 1)
	# The very beginning of month N
	thisM = datetime(post_year,post_month,1)
	# The very beginning of month N+1
	nextM = datetime((post_year if post_month != 12 else post_year+1),(post_month+1 if post_month != 12 else 1), 1)
	# posts = db.GqlQuery("""SELECT * FROM Post WHERE post_on >:1 AND post_on <:2 ORDER BY post_on DESC""", thisM, nextM)
	# month_view = db.GqlQuery("""SELECT * FROM Post WHERE post_on >:1 AND post_on <:2 ORDER BY post_on DESC""", thisM, nextM)
	# posts =  getcached('Post', lambda: models.Post.all(), expiration=3600)
	posts = models.Post.gql("""WHERE post_on >:1 AND post_on <:2 ORDER BY post_on DESC""", thisM, nextM)	
	recent_comments= getcached('Comments', lambda: models.Comments.all().order('-comments_post_on').fetch(5), expiration=3600)
	sitelink = getcached('SiteLink', lambda: models.SiteLink.all(), expiration=3600)
	featurelink = getcached('FeatureLink', lambda: models.FeatureLink.all(), expiration=3600)
	tag_cloud = getcached('BlogTag', lambda: models.BlogTag.all(), expiration=3600)
	articles =  models.Post.all().filter('article',True)
	cats=models.Cat.all()	
	payload = dict(recent_comments=recent_comments,
					sitelink=sitelink,
					featurelink=featurelink,
					tag_cloud=tag_cloud,
					cats=cats,
					greeting=greeting,
					posts = posts,
					blog_view = 'archive',
					)
	return render('index.html', payload)
	


def catagory(request,cat_slug,page=1):
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
		
	all_posts = getcached('Post', lambda: models.Post.all(), expiration=3600)
	thecats = models.Cat.all().filter('slug = ',cat_slug).fetch(1)
	catkey = thecats[0]
	posts = all_posts.order('-post_on').filter('cat',catkey.key())
		
	try:
		page = int(page)-1
	except:
		page = 0
	show_prev = False
	show_next = False
	paginator = ObjectPaginator(posts,10)
	if page >= paginator.pages:
		page = paginator.pages - 1
	posts_page=paginator.get_page(page)
	pages=range(1,paginator.pages+1)	
	show_prev = paginator.has_previous_page(page)
	show_next = paginator.has_next_page(page)
	page=page+1	
		
	blog_view = 'catagory'
	blog_slug = cat_slug
	recent_comments= getcached('Comments', lambda: models.Comments.all().order('-comments_post_on').fetch(5), expiration=3600)
	sitelink = getcached('SiteLink', lambda: models.SiteLink.all(), expiration=3600)
	featurelink = getcached('FeatureLink', lambda: models.FeatureLink.all(), expiration=3600)
	tag_cloud = getcached('BlogTag', lambda: models.BlogTag.all(), expiration=3600)
	articles =  models.Post.all().filter('article',True)
	cats=models.Cat.all()
	payload = dict(cats=cats,
					recent_comments=recent_comments,
					articles=articles,
					featurelink=featurelink,tag_cloud=tag_cloud,
					sitelink=sitelink,
					show_edit=show_edit,
					greeting=greeting,
					pages=pages,
					page=page,
					show_prev = show_prev,
					show_next = show_next,
					prev = page - 1,
					next = page + 1,
					posts = posts_page,
					blog_view = blog_view,
					blog_slug = blog_slug
					)
	return render('index.html', payload)


def index(request,page=1):
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

	try:
		page = int(page)-1
	except:
		page = 0
	show_prev = False
	show_next = False
	all_posts = models.Post.all().order('-post_on')
	paginator = ObjectPaginator(all_posts,10)
	if page >= paginator.pages:
		page = paginator.pages - 1
	posts=paginator.get_page(page)
	pages=range(1,paginator.pages+1)	
	show_prev = paginator.has_previous_page(page)
	show_next = paginator.has_next_page(page)
	page=page+1	
	
	blog_view = 'page'
	
#	recent_comments= getcached('Comments', lambda: models.Comments.all().order('-comments_post_on').fetch(5), expiration=3600)
#	sitelink = getcached('SiteLink', lambda: models.SiteLink.all(), expiration=3600)
#	featurelink = getcached('FeatureLink', lambda: models.FeatureLink.all(), expiration=3600)
#	tag_cloud = getcached('BlogTag', lambda: models.BlogTag.all(), expiration=3600)
	
	recent_comments = models.Comments.all().order('-comments_post_on').fetch(5)
	sitelink = models.SiteLink.all()
	featurelink = models.FeatureLink.all()
	tag_cloud = models.BlogTag.all()
	articles =  models.Post.all().filter('article',True)
	cats=models.Cat.all()
	
	
	payload = dict(cats=cats,
					recent_comments=recent_comments,
					articles=articles,
					featurelink=featurelink,
					tag_cloud=tag_cloud,
					sitelink=sitelink,
					show_edit=show_edit,
					greeting=greeting,
					posts=posts,
					pages=pages,
					page=page,
					show_prev = show_prev,
					show_next = show_next,
					prev = page - 1,
					next = page + 1,
					blog_view = blog_view ,
					)
	return render('index.html', payload)


def comment(request, post_slug):
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
#	post = models.Post.get_by_key_name(slug)
	posts = models.Post.all().filter('slug =', post_slug).fetch(1)
	post = posts[0]
	comments = models.Comments.all().filter('post =',post)
	if user:
		if request.method == 'POST':
			commentform = bforms.CommentFormUser(request.POST)
			if commentform.is_valid():				
				comment = commentform.save(post,user)
				return HttpResponseRedirect('/post/%s'%post_slug)
		else:
			commentform = bforms.CommentFormUser()
	else:
		if request.method == 'POST':
			commentform = bforms.CommentForm(request.POST)
			if commentform.is_valid():				
				comment = commentform.save(post)
				return HttpResponseRedirect('/post/%s'%post_slug)
		else:
			commentform = bforms.CommentForm()
	cats = models.Cat.all()
	sitelink = models.SiteLink.all()
	featurelink = models.FeatureLink.all()
	tag_cloud = models.BlogTag.all()
	articles =  models.Post.all().filter('article',True)
	friendsconnect = False
	payload = dict(cats=cats,friendsconnect=friendsconnect,articles=articles,featurelink=featurelink,tag_cloud=tag_cloud,sitelink=sitelink,greeting=greeting,show_edit=show_edit,post=post,commentform=commentform,comments=comments)
	return render('single.html', payload)
	
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