from django import template
from datetime import datetime,timedelta
from google.appengine.api import users
import rfc3339
register = template.Library()

def timezone(value, offset):
	return value + timedelta(hours=offset)
	
register.filter(timezone)

def jieblognickname(value):
	nick = value.nickname().split("@")
	return nick[0]

register.filter(jieblognickname)

def get_rfc_datetime(datetime_data):
	return rfc3339.rfc3339(datetime_data)
	
register.filter(get_rfc_datetime)

def gendes(contents,length=50):
	n = int(length)
	content = contents[:n]
	return content

register.filter(gendes)