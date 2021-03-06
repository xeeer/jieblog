﻿from django.http import HttpResponse, HttpResponseRedirect
from jieblog.applications import models
from jieblog.applications import bforms
from google.appengine.api import users
from google.appengine.ext import db
from funcs import render

def Config(request):
	user = users.get_current_user()
	if users.is_current_user_admin():
		keyname="blog"
		site = models.Site.get_or_insert(keyname)
		if request.method == 'POST':
			siteform = bforms.SiteForm(request.POST)
			if siteform.is_valid():
				siteform.save(site)
				return HttpResponseRedirect('/admin/config')
		else:
			siteform = bforms.SiteForm(initial={'site_title':site.site_title,
											'sub_title':site.sub_title,
											'site_copyright':site.site_copyright,
											'post_per_page':site.post_per_page,
											'owner_name':site.owner_name,
											'code_license':site.code_license,
											'content_license':site.content_license})
	else:
		return  HttpResponseRedirect('/login')
	payload = dict(siteform = siteform)
	return render('AdminConfig.html', payload)

def PostCat(request):
	user = users.get_current_user()
	cats = models.Cat.all()
	if users.is_current_user_admin():
		if request.method == 'POST':
			catform = bforms.CatForm(request.POST)
			if catform .is_valid():
				cat = catform .save()
				return HttpResponseRedirect('/admin/cat')
		else:
			catform = bforms.CatForm()
	else:
		return  HttpResponseRedirect('/login')
	payload = dict(catform = catform,cats=cats)
	return render('AdminCat.html', payload)

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
	return render('AdminManage.html',payload)


def delete_post(request,post_id):
	user = users.get_current_user()
	if users.is_current_user_admin():
		post = models.Post.get_by_id(int(post_id))
		post.delete()
	else:
		return HttpResponseRedirect('/login')
	return HttpResponseRedirect('/list')

def delete_cat(request,cat_id):
	user = users.get_current_user()
	if users.is_current_user_admin():
		cat = models.Cat.get_by_id(int(cat_id))
		cat.delete()
	else:
		return HttpResponseRedirect('/login')
	return HttpResponseRedirect('/admin/cat')

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
	return render('AdminDashboard.html', payload)
#	return render_to_response('create.html',{'postform':postform})

def edit(request,post_id):
	user = users.get_current_user()
	if users.is_current_user_admin():
		post = models.Post.get_by_id(int(post_id))
		cat_data = models.Cat.get(post.cat.key()).key()
		s = ",".join(["%s" %i for i in post.tags])
		postform = bforms.EditForm(initial={'article':post.article,'draft':post.draft,'title':post.title,'content':post.content,'tags':s,'slug':post.slug,'cat':cat_data})
		if request.method == 'POST':
			postform = bforms.EditForm(request.POST)
			if postform.is_valid():
				postform.save(post)
				return HttpResponseRedirect('/post/%s' %post.slug)
	else:
		return HttpResponseRedirect('/login')
	payload = dict(postform=postform)
	return render('AdminDashboard.html', payload)

def edit_cat(request,cat_id):
	user=users.get_current_user()
	cats=models.Cat.all()
	if users.is_current_user_admin():
		cat=models.Cat.get_by_id(int(cat_id))
		catform=bforms.CatForm(initial={'name':cat.name,'slug':cat.slug})
		if request.method == 'POST':
			catform = bforms.CatForm(request.POST)
			if catform.is_valid():
				catform.edit(cat)
				return HttpResponseRedirect('/admin/cat')
	else:
		return HttpResponseRedirect('/login')
	payload = dict(catform=catform,cats=cats)
	return render('AdminCat.html',payload)

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

