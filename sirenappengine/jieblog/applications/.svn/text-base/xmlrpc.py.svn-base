# Patchless XMLRPC Service for Django
# Kind of hacky, and stolen from Crast on irc.freenode.net:#django
# Self documents as well, so if you call it from outside of an XML-RPC Client
# it tells you about itself and its methods
#
# Brendan W. McAdams <brendan.mcadams@thewintergrp.com>

# SimpleXMLRPCDispatcher lets us register xml-rpc calls w/o
# running a full XMLRPC Server.  It's up to us to dispatch data

from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse
import os
from datetime import datetime
from models import *
from google.appengine.api import users

# Create a Dispatcher; this handles the calls and translates info to function maps
#dispatcher = SimpleXMLRPCDispatcher() # Python 2.4
dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None) # Python 2.5
ROOT_PATH = os.path.dirname(__file__)


def rpc_handler(request):
	"""
	the actual handler:
	if you setup your urls.py properly, all calls to the xml-rpc service
	should be routed through here.
	If post data is defined, it assumes it's XML-RPC and tries to process as such
	Empty post assumes you're viewing from a browser and tells you about the service.
	"""

	response = HttpResponse()
	if len(request.POST):
		response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
	if request.method == 'GET':
		response.write("<b>This is an XML-RPC Service.</b><br>")
		response.write("You need to invoke it using an XML-RPC Client!<br>")
		response.write("The following methods are available:<ul>")
		methods = dispatcher.system_listMethods()

		for method in methods:
			# right now, my version of SimpleXMLRPCDispatcher always
			# returns "signatures not supported"... :(
			# but, in an ideal world it will tell users what args are expected
			sig = dispatcher.system_methodSignature(method)

			# this just reads your docblock, so fill it in!
			help =  dispatcher.system_methodHelp(method)

			response.write("<li><b>%s</b>: [%s] %s" % (method, sig, help))

		response.write("</ul>")
		response.write('<a href="http://www.djangoproject.com/"> <img src="http://media.djangoproject.com/img/badges/djangomade124x25_grey.gif" border="0" alt="Made with Django." title="Made with Django."></a>')

	response['Content-length'] = str(len(response.content))
	return response



def check_admin(username,password):
	if username=='lucidanui@gmail.com' and password=='123456':
		return username

def blogger_getUsersBlogs(discard,username, password,):
		return [{'url' :ROOT_PATH, 'blogid' : '001', 'blogName' : 'jieblog'}]

def metaWeblog_newPost(blogid, username, password, content, publish):
		user = users.User(check_admin(username, password))
		if not user:
				raise Exception, 'access denied'
				
		if content.has_key('categories'):
			tags = content['categories']
		else:
			tags = []
		if publish:
			the_post = Post(title = content['title'], content = content['description'], author = user, tags = tags)
			key = the_post.put()
			return str(key.id())
		else:
			return 'notpublished'
				
def metaWeblog_editPost(postid, username, password, content, publish):
		user = users.User(check_admin(username, password))
		if not user:
			raise Exception, 'access denied'

		if publish:
			the_post = Post.get_by_id(int(postid))
			the_post.title = content['title']
			the_post.content = content['description']
			the_post.author = user
			the_post.tags = content['categories']
			the_post.put()
			return True
		else:
			return True

def metaWeblog_getCategories(blogid, username, password):
		user = check_admin(username, password)
		if not user:
			raise Exception, 'access denied'

		categories = []
		all_tags = BlogTag.all()
		for tag in all_tags:
			categories.append({'description' : tag.name, 'title' : tag.name})

		return categories

def metaWeblog_getPost(postid, username, password):
		user = check_admin(username, password)
		if not user:
			raise Exception, 'access denied'

		post = Post.get_by_id(int(postid))

		return {
					'postid' : postid,
					'dateCreated' : post.post_on,
					'title' : post.title,
					'description' : unicode(post.content),
					'categories' : post.tags,
					'publish' : True,
				}

def metaWeblog_getRecentPosts(blogid, username, password, numberOfPosts):
		posts = Post.all().order('-date').fetch(min(numberOfPosts, 20))
		result = []
		for post in posts:
			result.append({
				'postid' : str(post.key().id()),
				'dateCreated' : post.date,
				'title' : post.title,
				'description' : unicode(post.content),
				'categories' : post.tags,
				'publish' : True,
				})

		return result


def blogger_deletePost(appkey, postid, username, password, publish):
		user = check_admin(username, password)
		if not user:
			raise Exception, 'access denied'

		post = Post.get_by_id(int(postid))
		post.delete()
		return True


dispatcher.register_function(blogger_getUsersBlogs,'blogger.getUsersBlogs')
dispatcher.register_function(metaWeblog_newPost,'metaWeblog.newPost')
dispatcher.register_function(metaWeblog_editPost,'metaWeblog.editPost')
dispatcher.register_function(metaWeblog_getCategories,'metaWeblog.getCategories')
dispatcher.register_function(metaWeblog_getPost,'metaWeblog.getPost')
dispatcher.register_function(blogger_deletePost,'blogger.deletePost')
