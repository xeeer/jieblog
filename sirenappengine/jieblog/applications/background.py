from django.http import HttpResponse, HttpResponseRedirect
from jieblog.applications import models
from jieblog.applications import bforms
from google.appengine.api import users
from google.appengine.ext import db

from funcs import render

def list_post(request,page=0):
	user = users.get_current_user()
	if users.is_current_user_admin():
		pass
	else:
		return HttpResponseRedirect('/login')
	page = int(page)
	posts_per_page = 20
	show_prev = False
	show_next = False
	all_posts = models.Post.all()
	max_page = (all_posts.count()-1) / posts_per_page
	posts = all_posts.order('-post_on').fetch(posts_per_page, offset = page * posts_per_page)
	show_prev = not (page == 0)
	show_next = not (page == max_page)
	if not posts:
		show_prev = False
		show_next = False
	current_page = page + 1
	payload = dict(posts=posts,show_prev=show_prev,show_next = show_next,show_page_panel = show_prev or show_next,prev = page - 1,next = page + 1,current_page = current_page)
	return render('post_list.html',payload)


def delete_post(request,post_id):
	user = users.get_current_user()
	if users.is_current_user_admin():
		post = models.Post.get_by_id(int(post_id))
		post.delete()
	else:
		return HttpResponseRedirect('/login')
	return HttpResponseRedirect('/list')


def create(request):
	user = users.get_current_user()
	if users.is_current_user_admin():
		if request.method == 'POST':
			postform = bforms.PostForm(request.POST)
			if postform.is_valid():
				post = postform.save(user)
				return HttpResponseRedirect('/')
		else:
			postform = bforms.PostForm()
	else:
		return  HttpResponseRedirect('/login')
	payload = dict(postform = postform)
	return render('admin.html', payload)
#	return render_to_response('create.html',{'postform':postform})

def edit(request,post_id):
	user = users.get_current_user()
	if users.is_current_user_admin():
		post = models.Post.get_by_id(int(post_id))
		s = ",".join(["%s" %i for i in post.tags])
		postform = bforms.EditForm(initial={'article':post.article,'draft':post.draft,'title':post.title,'content':post.content,'tags':s})
		if request.method == 'POST':
			postform = bforms.EditForm(request.POST)
			if postform.is_valid():
				postform.save(post)
				return HttpResponseRedirect('/post/%s' %post_id)
	else:
		return HttpResponseRedirect('/login')
	payload = dict(postform=postform)
	return render('admin.html', payload)
	
def login(request):
	user = users.get_current_user()
	if user:
		greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
				  (user.nickname(), users.create_logout_url("/")))
	else:
		greeting = ("<a href=\"%s\">Sign in or register</a>." %
				  users.create_login_url("/"))
	payload = dict(greeting=greeting)
	return render('admin-login.html',payload)

	
