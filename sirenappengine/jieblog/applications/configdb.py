from django.http import HttpResponse, HttpResponseRedirect
from jieblog.applications import models
from jieblog.applications import bforms
from funcs import render
from google.appengine.api import users
from google.appengine.ext import db

def setupdb(request):
	user = users.get_current_user()
	if users.is_current_user_admin():
		if request.method == 'POST':
			configform = bforms.ConfigForm(request.POST)
			sitelinkform = bforms.SiteLinkForm(request.POST)

			if configform.is_valid():
				configform.save()
				return HttpResponseRedirect('/config')

			if sitelinkform.is_valid():
				sitelinkform.save()
				return HttpResponseRedirect('/config')
		else:
			configform = bforms.ConfigForm()
			sitelinkform = bforms.SiteLinkForm()
	else:
		return HttpResponseRedirect('/login')
	payload = dict(configform = configform,sitelinkform=sitelinkform)
	return render('config-form.html', payload)

def configdb(request,post_id):
	user = users.get_current_user()
	if users.is_current_user_admin():
		configdb = models.ConfigDB.get_by_id(int(post_id))
		if request.method == 'POST':
			configform = bforms.ConfigForm(initial={'name':config.name,'subtitle':config.subtitle,'post_per_page':config.post_per_page})

			sitelinkform = bforms.SiteLinkForm(request.POST)
			if configform.is_valid():
				configform.safe(config)
				return HttpResponseRedirect('/config')
			
			if sitelinkform.is_valid():
				sitelinkform.save()
				return HttpResponseRedirect('/')
			
		else:
			configform = bforms.ConfigForm()
			sitelinkform = bforms.SiteLinkForm()
	else:
		return HttpResponseRedirect('/login')
	payload = dict(configform = configform,sitelinkform=sitelinkform)
	return render('config-form.html', payload)

