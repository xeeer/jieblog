from django.shortcuts import render_to_response
from google.appengine.api import memcache
from google.appengine.ext import db
from jieblog.applications import models
import re

def render(template, payload):
	return render_to_response(template, payload)
	
def split_tags(s):
		tags = list(set([t.strip() for t in re.split('[,;\\/\\\\]*', s) if t != ''])) #uniq
		return tags
		
		
def get_data(the_key, time_exp):
  data = memcache.get("Post")
  if data is not None:
	return data
  else:
	data = query_for_data()
	if not memcache.add(the_key, data, time_exp):
		logging.error("Memcache set failed.")
	return data
	
def query_for_data():
	results = models.Post.all()
#	results = db.GqlQuery("SELECT * "
#						  "FROM Post "
#						  "ORDER BY date DESC").fetch(10)
	return results