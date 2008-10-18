from django import template
from datetime import datetime,timedelta
from google.appengine.api import users
register = template.Library()

def timezone(value, offset):
	return value + timedelta(hours=offset)
	
register.filter(timezone)

def jieblognickname(value):
	nick = value.nickname().split("@")
	return nick[0]

register.filter(jieblognickname)