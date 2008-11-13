from django.shortcuts import render_to_response
import re

def render(template, payload):
	return render_to_response(template, payload)
	
def split_tags(s):
		tags = list(set([t.strip() for t in re.split('[,;\\/\\\\]*', s) if t != ''])) #uniq
		return tags