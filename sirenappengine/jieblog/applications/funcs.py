from django.shortcuts import render_to_response
from google.appengine.api import memcache
from google.appengine.ext import db
from jieblog.applications import models
import re
import logging
import sys

def get_cat():
	return ((thelist.slug,thelist.name) for thelist in models.Cat.all())

def render(template, payload):
	return render_to_response(template, payload)
	
def split_tags(s):
		tags = list(set([t.strip() for t in re.split('[,;\\/\\\\]*', s) if t != ''])) #uniq
		return tags
		
		
def memcache_get_post_data(the_key, time_exp):
  data = memcache.get(the_key)
  if data is not None:
	return data
  else:
	data = query_posts_data(the_key)
	if not memcache.add(the_key, data):
		logging.error("Memcache set failed.")
	return data
	
def query_posts_data(the_key):
	key = the_key % args[0:the_key.count('%')]
	results = models.key.all()
#	results = db.GqlQuery("SELECT * "
#						  "FROM Post "
#						  "ORDER BY date DESC").fetch(10)
	return results
	

def getcached(key, gen, expiration=0):
	logging.debug("cache-fetching %s"%key)
	try:
		s = memcache.get(key)
	except:
		logging.warn("ERROR on get: %s",sys.exc_info()[0])
		s = None
	if s is None:
		logging.debug("Cache miss for %s"%key)
		s = gen()
		logging.debug("gen() returned %r"%s)
		memcache.Client().set(key, s, expiration)
	else:
		logging.debug("Cache hit for %s"%key)
		return s